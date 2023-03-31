from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cws2.models.base import (
    AutoSlugMixin,
    TransientModel,
    TransientModelManager,
    OwnableModel,
    UUIDModel,
)
from cws2.constants import LanguageStatus, LanguageType


class Language(AutoSlugMixin, TransientModel, OwnableModel, UUIDModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=64,
        db_index=True,
        help_text=_("This is the name of your language, in English."),
    )
    slug = models.SlugField(
        verbose_name=_("Identifier"),
        max_length=64,
        db_index=True,
        blank=True,
        unique=True,
        help_text=_(
            "This is like a username for your language, appearing in your language "
            "page's URL. You may not have more than one language with the same "
            "identifier."
        ),
    )
    endonym = models.CharField(
        verbose_name=_("Endonym"),
        max_length=128,
        blank=True,
        db_index=True,
        help_text=_(
            "This is the name of your language, in your language. Don't worry if "
            "you don't know this yet - you can leave this field blank."
        ),
    )
    code = models.CharField(
        verbose_name=_("Language code"),
        max_length=6,
        blank=True,
        help_text=_(
            "An abbreviation or ISO-style code for this language, if you have one. "
            "This is purely cosmetic."
        ),
    )
    language_type = models.CharField(
        verbose_name=_("Language type"),
        max_length=3,
        choices=LanguageType.CHOICES,
        default=LanguageType.NOT_SPECIFIED,
        help_text=_("Select the language type that best represents your language."),
    )
    language_status = models.CharField(
        verbose_name=_("Language status"),
        max_length=1,
        choices=LanguageStatus.CHOICES,
        default=LanguageStatus.NEW,
        help_text=_("What stage of development is your language at?"),
    )
    description = models.TextField(
        verbose_name=_("Summary"),
        blank=True,
        help_text=_(
            "This is a brief summary of your language that will appear on its page. "
            "You can write more specific articles about the language later on."
        ),
    )
    is_natural = models.BooleanField(
        verbose_name=_("Natural language status"),
        default=False,
        db_index=True,
        help_text=_("Is this a natural language, rather than a constructed language?"),
    )

    objects = TransientModelManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owned_by", "slug"],
                name="cws2_language_unique_owner_slug",
            )
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "language.show",
            kwargs={"user": self.created_by.username, "language": self.slug},
        )
