from datetime import datetime

from django.db import models
from django_extensions.db.fields import ShortUUIDField


class TransientModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(archived_at__isnull=True)

    def archived(self):
        return super().get_queryset().filter(archived_at__isnull=False)


class TransientModel(models.Model):
    """Defines a model that can be created, updated and soft deleted, with
    datetime fields to track these actions.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived_at = models.DateTimeField(null=True)

    def archive(self):
        self.archived_at = datetime.now()

    def unarchive(self):
        self.archived_at = None

    @property
    def archived(self):
        return self.archived_at is not None

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
