from django.db import models
from django.utils.translation import gettext_lazy as _

from cws2.constants import PartOfSpeech
from cws2.models.base import TransientModel, TransientModelManager, UUIDModel


class WordClass(TransientModel):
    """
    Represents a specific word class that may be applied to a word in a user's
    language.
    """

    language = models.ForeignKey(
        "Language",
        on_delete=models.CASCADE,
        db_index=True,
        related_name="classes",
        verbose_name=_("Language"),
        help_text=_("The language to which this word class belongs."),
    )
    label = models.CharField(
        max_length=64,
        verbose_name=_("Label"),
        help_text=_(
            "The label for this word class, e.g. 'masculine' or 'imperfective'."
        ),
    )

    objects = TransientModelManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["language", "label"], name="cws2_wordclass_language_label"
            )
        ]

    def __str__(self):
        return f"{self.label} ({self.language.name})"


class Word(TransientModel, UUIDModel):
    """Represents a single word in a user's language."""

    language = models.ForeignKey(
        "Language",
        on_delete=models.CASCADE,
        db_index=True,
        related_name="words",
        verbose_name=_("Language"),
        help_text=_("The language to which is this word belongs."),
    )
    dialect = models.ForeignKey(
        "Dialect",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_index=True,
        related_name="words",
        verbose_name=_("Dialect"),
        help_text=_(
            "If this word belongs to a specific dialect, you can set that here."
        ),
    )
    headword = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_("Word"),
        help_text=_(
            "The word in your language. Double check you don't already have this word!"
        ),
    )
    alt_word = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Alternative word"),
        help_text=_(
            "An alternative written form of this word. Useful if your language uses "
            "more than one script."
        ),
    )
    ipa = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Pronunciation (IPA)"),
        help_text=_(
            "The pronunciation of this word in the International Phonetic Alphabet. "
            "Enter this as just IPA, without any enclosing brackets."
        ),
    )
    xsampa = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Pronunciation (X-SAMPA)"),
        help_text=_(
            "The pronunciation of this word in X-SAMPA. Enter this as just X-SAMPA, "
            "without any enclosing brackets."
        ),
    )
    source_language = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_("Source language"),
        help_text=_(
            "The language from which this word is derived or borrowed. Feel free to "
            "leave this blank, or use the 'etymology' field to give more detailed "
            "information."
        ),
    )
    etymology = models.TextField(
        blank=True,
        verbose_name=_("Etymology"),
        help_text=_("An optional explanation of how this word came to be."),
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes"),
        help_text=_(
            "Any other notes that might be useful for understanding this dictionary "
            "entry."
        ),
    )
    reference_image = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Image link"),
        help_text=_(
            "The URL of a reference image that can be displayed with the word "
            "summary. Useful for conscripts and sign-languages."
        ),
    )
    roots = models.ManyToManyField(
        "Word",
        blank=True,
        verbose_name=_("Roots"),
        help_text=_("Any words from which this word derives."),
    )

    objects = TransientModelManager()

    def __str__(self):
        return f"{self.headword} ({self.language.name})"


class WordDefinition(TransientModel):
    """Represents a single definition for a word."""

    word = models.ForeignKey(
        "Word",
        on_delete=models.CASCADE,
        db_index=True,
        related_name="definitions",
        verbose_name=_("Word"),
        help_text=_("The word to which this definition belongs."),
    )
    part_of_speech = models.CharField(
        max_length=3,
        verbose_name=_("Part of speech"),
        choices=PartOfSpeech.CHOICES,
        help_text=_(
            "The part of speech for this definition of the word. If there's no exact "
            "match, just pick whichever is the closest."
        ),
    )
    register = models.CharField(
        max_length=4,
        blank=True,
        verbose_name=_("Register"),
        help_text=_(
            "Here you can optionally specify the social register of this word, i.e. "
            "what specific context does this word belong to?"
        ),
    )
    definition = models.TextField(
        verbose_name=_("Definition"),
        help_text=_(
            "If possible, keep this as succinct as possible. You can always add extra "
            "definitions to this word."
        ),
    )
    classes = models.ManyToManyField(
        "WordClass",
        blank=True,
        verbose_name=_("Classes"),
        help_text=_(
            "Any classes to which this word belongs. If the classes have tables "
            "defined, these will be shown on the word's page."
        ),
    )

    objects = TransientModelManager()

    def __str__(self):
        return f"{self.word.headword}: {self.definition}"


class WordExample(TransientModel):
    definition = models.ForeignKey(
        "WordDefinition",
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name=_("Definition"),
        help_text=_("The word definition to which this example belongs."),
    )
    text = models.TextField(
        verbose_name=_("Example text"),
        help_text=_("This is the example containing this sense of the word."),
    )
    translation = models.TextField(
        blank=True,
        verbose_name=_("Example translation"),
        help_text=_(
            "Optionally, you can put the English translation of the example here."
        ),
    )

    objects = TransientModelManager()

    def __str__(self):
        return self.text
