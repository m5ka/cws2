from django.db import models
from django_extensions.db.fields import ShortUUIDField


class UpdatableModel(models.Model):
    """Defines a model which holds information on when
    it was created and last updated.
    """

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Defines a model whose primary key is a Short UUID."""

    uuid = ShortUUIDField(
        max_length=22,
        primary_key=True,
    )

    class Meta:
        abstract = True
