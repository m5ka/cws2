from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cws2.constants import GroupAccessType
from cws2.models.base import (
    AutoSlugMixin,
    TransientModel,
    TransientModelManager,
    UUIDModel,
)
from cws2.validators import (
    validate_colour_code_regex,
    validate_username_length,
    validate_username_regex,
)


class Group(AutoSlugMixin, UUIDModel, TransientModel):
    """Represents a meaningful group of Users."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=64,
        db_index=True,
        help_text=_("What should this group be called."),
    )
    slug = models.SlugField(
        verbose_name=_("Identifier"),
        max_length=64,
        db_index=True,
        blank=True,
        unique=True,
        help_text=_(
            "This is a unique group identifier that will appear in the group's URL."
        ),
    )
    icon = models.CharField(
        verbose_name=_("Icon character"),
        max_length=1,
        default="✱",
        help_text=_("A single character to represent the group in its icon."),
    )
    icon_colour_bg = models.CharField(
        verbose_name=_("Icon background colour"),
        max_length=7,
        default="#28A745",
        validators=[validate_colour_code_regex],
        help_text=_("The background colour of this group's icon."),
    )
    icon_colour_fg = models.CharField(
        verbose_name=_("Icon foreground colour"),
        max_length=7,
        default="#FFFFFF",
        validators=[validate_colour_code_regex],
        help_text=_("The foreground colour of this group's icon."),
    )
    access_type = models.CharField(
        verbose_name=_("Access type"),
        max_length=1,
        choices=GroupAccessType.CHOICES,
        help_text=_("Who should be allowed to join this group, and how?"),
    )
    is_hidden = models.BooleanField(
        verbose_name=_("Hidden status"),
        default=False,
        help_text=_("Should this group be hidden from community group lists."),
    )
    is_everyone = models.BooleanField(
        verbose_name=_("Automatic-join status"),
        default=False,
        db_index=True,
        help_text=_("Should all users automatically be part of this group?"),
    )

    objects = TransientModelManager()

    def __str__(self):
        return self.name

    def add_user(self, user, permissions=[], invited_by=None):
        """Adds a user to this group with the given permissions."""
        membership, new = GroupMembership.objects.get_or_create(
            group=self,
            user=user,
            defaults={
                "permissions": permissions,
                "invited_by": invited_by or User.objects.get(username="sheep"),
            },
        )
        if not new:
            membership.add_permissions(permissions)
            membership.save()
        return membership


class GroupMembership(models.Model):
    """Represents the many-to-many relationship in which a user belongs to a group.

    This relationship contains the user's permissions in the group as well as
    information about their joining of the group.
    """

    group = models.ForeignKey(
        "Group",
        on_delete=models.CASCADE,
        related_name="users",
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    permissions = ArrayField(
        models.CharField(
            max_length=32,
        ),
        verbose_name=_("Permissions in group"),
        default=list,
        blank=True,
        help_text=_("The permissions this user has in the group."),
    )
    joined_at = models.DateTimeField(
        auto_now_add=True,
    )
    invited_by = models.ForeignKey(
        "User",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        db_column="invited_by_user_id",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "user"],
                name="cws2_groupmembership_group_user",
            )
        ]

    def __str__(self):
        return f"@{self.user} ({self.group})"

    def add_permissions(self, permissions=[]):
        self.permissions = list(set(self.permissions + permissions))


class UserManager(BaseUserManager):
    """Manages Users by pre-fetching their profile."""

    def get_queryset(self):
        return super().get_queryset().select_related("profile")


class User(UUIDModel, AbstractUser):
    """Represents a user of the website."""

    username = models.CharField(
        verbose_name=_("Username"),
        max_length=64,
        unique=True,
        db_index=True,
        validators=[validate_username_length, validate_username_regex],
        help_text=_(
            "This is the unique identifier you'll use to log in. It may only "
            "contain letters, numbers, hyphens, dashes and dots."
        ),
    )
    email = models.EmailField(
        verbose_name=_("Email address"),
        max_length=128,
        unique=True,
        help_text=_(
            "This should be your email address. Make sure it's valid and that you "
            "have access to it."
        ),
    )
    email_confirmed_at = models.DateTimeField(
        blank=True,
        null=True,
    )
    display_name = models.CharField(
        verbose_name=_("Display name"),
        max_length=64,
        blank=True,
        help_text=_(
            "This name will appear instead of your username in some places on the "
            "site, if set."
        ),
    )
    is_bot = models.BooleanField(
        verbose_name=_("Bot status"),
        default=False,
        help_text=_(
            "If true, this user will be considered a staff-run bot account and will "
            "not be able to be logged in to."
        ),
    )
    last_seen_ip = models.CharField(
        verbose_name=_("Last seen IP"),
        blank=True,
        max_length=48,
        help_text=_("The last IP address this user used to log in."),
    )
    last_seen_route = models.CharField(
        verbose_name=_("Last seen route"),
        blank=True,
        max_length=64,
        help_text=_("The route name of the last page this user accessed."),
    )
    last_seen_at = models.DateTimeField(
        verbose_name=_("Last seen at"),
        blank=True,
        null=True,
        help_text=_("The last time this user accessed the site."),
    )

    first_name = None
    last_name = None

    objects = UserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        pk = self.pk
        super().save(*args, **kwargs)
        if not pk:
            self.add_to_default_groups()
            self.create_profile()

    def get_absolute_url(self):
        return reverse("user.show", kwargs={"user": self.username})

    @property
    def email_confirmed(self):
        return self.email_confirmed_at is not None

    def add_to_default_groups(self):
        """Adds this user to any default Groups, meaning any groups with `is_everyone`
        set to True.
        """
        for group in Group.objects.filter(is_everyone=True).all():
            group.add_user(self)

    def create_profile(self):
        """Creates a UserProfile object for this user if not already created."""
        UserProfile.objects.get_or_create(user=self)


class UserProfile(models.Model):
    """Contains customisable profile information for a user."""

    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        related_name="profile",
        primary_key=True,
    )
    pronouns = models.CharField(
        verbose_name=_("Pronouns"),
        max_length=64,
        blank=True,
        help_text=_("What pronouns should people use when referring to you?"),
    )
    location = models.CharField(
        verbose_name=_("Location"),
        max_length=64,
        blank=True,
        help_text=_("Where in the world are you?"),
    )
    bio = models.TextField(
        verbose_name=_("About me"),
        blank=True,
        help_text=_(
            "Write something about yourself! This will appear on your profile page."
        ),
    )

    def __str__(self):
        return f"@{self.user.username}"
