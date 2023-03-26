from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from cws2 import models


for model in [getattr(models, m) for m in models.__all__]:
    if model.__name__ != "User":
        admin.site.register(model)


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "preferred_name", "username", "password")}),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                    "email_confirmed",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
