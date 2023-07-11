from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Permission(models.Model):
    ownable_model = models.CharField(
        verbose_name=_("Ownable model"),
        max_length=64,
        help_text=_("The model name of the ownable resource."),
    )
    ownable_pk = models.BigIntegerField(
        verbose_name=_("Ownable ID"),
        help_text=_("The unique ID of the ownable resource."),
    )
    permissions = ArrayField(
        models.CharField(
            max_length=32,
        ),
        verbose_name=_("Permissions"),
        default=list,
        blank=True,
        help_text=_("The permissions granted for this resource."),
    )
    granted_by = models.ForeignKey(
        "User",
        null=True,
        on_delete=models.SET_NULL,
        db_column="granted_by_user_id",
        db_index=False,
        related_name="granted_%(class)ss+",
    )
    granted_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class UserPermission(Permission):
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="+",
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["ownable_model", "ownable_pk"],
            )
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["ownable_model", "ownable_pk", "user"],
                name="cws2_userpermission_unique_model_pk_user",
            )
        ]

    def __str__(self):
        return (
            f"<UserPermission: {self.user} on {self.ownable_model}:"
            f"{self.ownable_pk}>"
        )


class GroupPermission(Permission):
    group = models.ForeignKey(
        "Group",
        on_delete=models.CASCADE,
        related_name="+",
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["ownable_model", "ownable_pk"],
            )
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["ownable_model", "ownable_pk", "group"],
                name="cws2_grouppermission_unique_model_pk_user",
            )
        ]

    def __str__(self):
        return (
            f"<GroupPermission: {self.group} on {self.ownable_model}:"
            f"{self.ownable_pk}>"
        )
