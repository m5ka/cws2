from datetime import datetime

import shortuuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from slugify.slugify import slugify

from cws2.models.permission import GroupPermission, UserPermission


class AutoSlugMixin:
    """A mixin class that adds functionality for an auto-generated
    slug field.
    """

    auto_slug_field = "slug"
    auto_slug_populate_from = "name"

    def save(self, *args, **kwargs):
        existing = getattr(self, self.auto_slug_field)
        if not existing:
            source = getattr(self, self.auto_slug_populate_from)
            if source:
                setattr(self, self.auto_slug_field, slugify(source))
        super().save(*args, **kwargs)


class TransientModelManager(models.Manager):
    """A manager for transient models that automatically fetches non-archived
    objects unless `archived()` is specifically called.
    """

    def get_queryset(self):
        return super().get_queryset().filter(archived_at__isnull=True)

    def archived(self):
        return super().get_queryset().filter(archived_at__isnull=False)


class TransientModel(models.Model):
    """Defines a model that can be created, updated and soft deleted, with
    datetime fields to track these actions.
    """

    created_by = models.ForeignKey(
        "User",
        null=True,
        on_delete=models.SET_NULL,
        related_name="created_%(class)ss",
        db_column="created_by_user_id",
        db_index=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_by = models.ForeignKey(
        "User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="updated_%(class)ss+",
        db_column="updated_by_user_id",
        db_index=False,
    )
    updated_at = models.DateTimeField(
        null=True,
        auto_now=True,
    )
    archived_by = models.ForeignKey(
        "User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="archived_%(class)ss+",
        db_column="archived_by_user_id",
        db_index=False,
    )
    archived_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def archive(self):
        self.archived_at = datetime.now()

    def unarchive(self):
        self.archived_at = None

    @property
    def archived(self):
        return self.archived_at is not None


class OwnableModel(models.Model):
    """Defines a model that can be owned by a user and shared with other users
    or groups according to set permissions."""

    owned_by = models.ForeignKey(
        "User",
        related_name="owned_%(class)ss",
        on_delete=models.PROTECT,
        db_column="owned_by_user_id",
        db_index=True,
    )
    is_public = models.BooleanField(
        verbose_name=_("Public status"),
        default=True,
        help_text=_(
            "Does everyone have an implicit read permission for this resource?"
        ),
    )
    is_shared = models.BooleanField(
        verbose_name=_("Sharing status"),
        default=False,
        help_text=_(
            "Are there specific user and group permissions set for this resource?"
        ),
    )

    class Meta:
        abstract = True

    def check_user_permission(self, user, permission):
        if self.owned_by == user:
            return True
        if self.is_public and permission == "read":
            return True
        if not self.is_shared:
            return False
        if UserPermission.objects.filter(
            ownable_model=self._meta.model_name,
            ownable_pk=self.pk,
            user=user,
            permissions__contains=[permission],
        ).exists():
            return True
        if GroupPermission.objects.filter(
            ownable_model=self._meta.model_name,
            ownable_pk=self.pk,
            group__users__user=user,
            permissions__contains=[permission],
        ).exists():
            return True
        return False


class UUIDModel(models.Model):
    """Defines a model containing a unique Short UUID."""

    uuid = models.CharField(
        max_length=22,
        unique=True,
        db_index=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = shortuuid.uuid()
        super().save(*args, **kwargs)
