from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cws2.models.base.abstracts import UUIDModel
from cws2.validators import validate_username_length, validate_username_regex


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

    first_name = None
    last_name = None

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def email_confirmed(self):
        return self.email_confirmed_at is not None

    def get_absolute_url(self):
        return reverse("user.show", kwargs={"user": self.username})
