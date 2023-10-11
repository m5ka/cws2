from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cws2.models.base import (
    UUIDModel,
)
from cws2.validators import (
    validate_username_length,
    validate_username_regex,
)


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
        Group = apps.get_model("cws2", "Group")
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
