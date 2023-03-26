from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from slugify.slugify import slugify

from cws2.models.base.abstracts import UpdatableModel, UUIDModel
from cws2.constants.choices import LanguageStatus, LanguageType


class Language(UpdatableModel, UUIDModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=64,
        help_text=_("This is the name of your language, in English."),
    )
    slug = AutoSlugField(
        verbose_name=_("Identifier"),
        populate_from="name",
        overwrite_on_add=False,
        slugify_function=slugify,
        max_length=64,
        db_index=True,
        blank=True,
        editable=True,
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
        help_text=_(
            "This is the name of your language, in your language. Don't worry if "
            "you don't know this yet - you can leave this field blank."
        ),
    )
    language_type = models.CharField(
        verbose_name=_("Language type"),
        max_length=16,
        choices=LanguageType.CHOICES,
        default=LanguageType.NOT_SPECIFIED,
        help_text=_("Select the language type that best represents your language."),
    )
    language_status = models.CharField(
        verbose_name=_("Language status"),
        max_length=16,
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
    created_by = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="languages",
    )

    class Meta:
        unique_together = ["created_by", "slug"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "language.show",
            kwargs={"user": self.created_by.username, "language": self.slug},
        )
