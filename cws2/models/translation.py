from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField

from cws2.models.base import TransientModel, TransientModelManager


class TranslationTemplate(TransientModel):
    """
    Represents a text that users can translate into their languages.
    """

    uuid = ShortUUIDField(
        verbose_name=_("UUID"),
        length=22,
        max_length=22,
        unique=True,
        db_index=True,
        help_text=_("The unique ID for this translation."),
    )
    name = models.CharField(
        max_length=64,
        verbose_name=_("Name"),
        help_text=_("A short name for this translation."),
    )
    text = models.TextField(
        verbose_name=_("Text"),
        help_text=_("The text that should be translated."),
    )
    source = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_("Source"),
        help_text=_("Where does this text come from?"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        help_text=_(
            "A description of the translation, giving some context or background."
        ),
    )

    objects = TransientModelManager()

    def get_absolute_url(self):
        return reverse("translation.show", kwargs={"translation": self.uuid})


class Translation(TransientModel):
    """
    Represents a translation of template into a specific language.
    """

    template = models.ForeignKey(
        "TranslationTemplate",
        on_delete=models.CASCADE,
        db_index=True,
        db_column="translation_template_id",
        related_name="translations",
        verbose_name=_("Template"),
        help_text=_("The template of which this is a translation."),
    )
    language = models.ForeignKey(
        "Language",
        on_delete=models.CASCADE,
        db_index=True,
        related_name="translations",
        verbose_name=_("Language"),
        help_text=_("The language this text is translated into."),
    )
    translation = models.TextField(
        verbose_name=_("Translation"),
        help_text=_("The translation of the text in your language."),
    )
    is_wip = models.BooleanField(
        default=False,
        verbose_name=_("Work in progress"),
        help_text=_(
            "Is this translation a work in progress? If you tick yes, it won't be "
            "visible to anyone else."
        ),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["template", "language"],
                name="cws2_translation_unique_template_language",
            )
        ]

    objects = TransientModelManager()
