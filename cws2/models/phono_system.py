from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from cws2.models.base import (
    TransientModel,
    TransientModelManager,
    OwnableModel,
    UUIDModel,
)
from cws2.constants import PhonoSystemStatus, PhoneCategory


class PhonoSystem(TransientModel, OwnableModel, UUIDModel):
    is_human = models.CharField(
        db_index=True,
        verbose_name=_("Default human phono system"),
        default=False,
        help_text=_("This is the name of the phono system."),
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=64,
        db_index=True,
        help_text=_("This is the name of the phono system."),
    )
    status = models.CharField(
        verbose_name=_("Phono system status"),
        max_length=1,
        choices=PhonoSystemStatus.CHOICES,
        default=PhonoSystemStatus.DRAFT,
        help_text=_("This is the status of the phono system."),
    )
    description = models.TextField(
        verbose_name=_("Summary"),
        blank=True,
        help_text=_(
            "This is a brief summary explaining the context of the phono system."
        ),
    )

    objects = TransientModelManager()

    def __str__(self):
        return f"'{self.name}' [Phono System={self.uuid}]"


class Phone(TransientModel, UUIDModel):
    glyph = models.CharField(
        verbose_name=_("Glyph"),
        max_length=12,
        help_text=_("This is a glyph that represents the phone."),
    )
    phono_system = models.ForeignKey(
        "PhonoSystem",
        on_delete=models.CASCADE,
        db_column="phono_system_id",
        db_index=True,
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=64,
        db_index=True,
        help_text=_("This is the name of the phone."),
    )
    category = models.CharField(
        verbose_name=_("Category"),
        max_length=1,
        choices=PhoneCategory.CHOICES,
        help_text=_("This is the status of the phono system."),
    )
    ipa = models.CharField(
        verbose_name=_("IPA"),
        max_length=12,
        help_text=_("This is the IPA phonetic representation of this phone."),
    )
    xsampa = models.CharField(
        verbose_name=_("X-Sampa"),
        max_length=12,
        help_text=_("This is the X-Sampa phonetic representation of this phone."),
    )
    tags = ArrayField(
        models.CharField(
            max_length=32,
        ),
        verbose_name=_("Tags"),
        default=list,
        blank=True,
        help_text=_("Tags associated with this phone."),
    )

    objects = TransientModelManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["phono_system_id", "glyph"],
                name="cws2_phone_unique_phono_system_glyph"),
        ]

    def __str__(self):
        return f"'{self.name}' [Phone={self.uuid}]"
