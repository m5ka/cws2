from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cws2.constants import GroupAccessType
from cws2.models.base import (
    AutoSlugMixin,
    OwnableModel,
    TransientModel,
    TransientModelManager,
    UUIDModel,
)
from cws2.models.user import User
from cws2.validators import validate_colour_code_regex


class Group(AutoSlugMixin, UUIDModel, OwnableModel, TransientModel):
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
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("An optional, brief overview on what this group is all about."),
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

    def get_absolute_url(self):
        return reverse("group.show", kwargs={"group": self.slug})

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

    def has_user(self, user):
        """Returns True if the group contains the given user as a member."""
        return GroupMembership.objects.filter(group=self, user=user).exists()


class GroupMembership(models.Model):
    """Represents the many-to-many relationship in which a user belongs to a group.

    This relationship contains the user's permissions in the group as well as
    information about their joining of the group.
    """

    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="users")
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="memberships"
    )
    permissions = ArrayField(
        models.CharField(max_length=32),
        verbose_name=_("Permissions in group"),
        default=list,
        blank=True,
        help_text=_("The permissions this user has in the group."),
    )
    joined_at = models.DateTimeField(auto_now_add=True)
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
                fields=["group", "user"], name="cws2_groupmembership_group_user"
            )
        ]

    def __str__(self):
        return f"@{self.user} ({self.group})"

    def add_permissions(self, permissions=[]):
        self.permissions = list(set(self.permissions + permissions))
