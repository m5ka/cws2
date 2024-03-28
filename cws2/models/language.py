from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cws2.constants import LanguageStatus, LanguageType
from cws2.models.base import (
    AutoSlugMixin,
    OwnableModel,
    TransientModel,
    TransientModelManager,
    UUIDModel,
)


def language_flag_path(instance, filename):
    fn = filename.split(".")
    if len(fn) > 1:
        ext = filename.split(".")[-1]
    else:
        ext = "png"
    return f"flags/{instance.created_by.username}__{instance.slug}.{ext}"


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
    language_flag = models.ImageField(
        blank=True,
        upload_to=language_flag_path,
        verbose_name=_("Language flag"),
        help_text=_(
            "An optional flag image that represents your language or the place it's "
            "spoken. Common flag ratios are recommended, such as 1:2, 2:3 or 3:5 "
            "(height to width). The image must be at least 100px wide and 50px high."
        ),
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
                fields=["owned_by", "slug"], name="cws2_language_unique_owner_slug"
            )
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "language.show",
            kwargs={"user": self.created_by.username, "language": self.slug},
        )


class Dialect(AutoSlugMixin, TransientModel, OwnableModel, UUIDModel):
    """Represents a specific dialect of a user's language."""

    language = models.ForeignKey(
        "Language",
        on_delete=models.CASCADE,
        verbose_name=_("Language"),
        help_text=_("The language to which this dialect belongs."),
    )
    name = models.CharField(
        max_length=64,
        db_index=True,
        verbose_name=_("Name"),
        help_text=_("This is the name of this dialect, in English."),
    )
    slug = models.SlugField(
        max_length=64,
        db_index=True,
        blank=True,
        unique=True,
        verbose_name=_("Identifier"),
        help_text=_(
            "This is like a username for this dialect, appearing in the dialect page's "
            "URL. You may not have more than one dialect for this language with the "
            "same identifier."
        ),
    )
    endonym = models.CharField(
        max_length=128,
        blank=True,
        db_index=True,
        verbose_name=_("Endonym"),
        help_text=_(
            "This is the name of this dialect, in your language. Don't worry if you "
            "don't know this yet - you can leave this field blank."
        ),
    )
    code = models.CharField(
        verbose_name=_("Dialect code"),
        max_length=6,
        blank=True,
        help_text=_(
            "An abbreviation or ISO-style code for this dialect, if you have one. "
            "This is purely cosmetic."
        ),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Summary"),
        help_text=_(
            "This is a brief summary of this dialect of your language that will appear "
            "on its page. You can write more specific articles about the dialect later "
            "on."
        ),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["language", "slug"], name="cws2_dialect_language_slug"
            )
        ]

    def __str__(self):
        return self.name
