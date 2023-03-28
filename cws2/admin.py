from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from cws2 import models


for model in [getattr(models, m) for m in models.__all__]:
    if model.__name__ != "User":
        admin.site.register(model)


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "display_name", "email", "password")}),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                    "is_bot",
                    "email_confirmed_at",
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
        ("Last seen", {"fields": ("last_seen_ip", "last_seen_route", "last_seen_at")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
