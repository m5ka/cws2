# Generated by Django 4.1.7 on 2023-03-27 20:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def generate_user_profiles(apps, schema_editor):
    User = apps.get_model("cws2", "User")
    UserProfile = apps.get_model("cws2", "UserProfile")
    for user in User.objects.select_related("profile").all():
        if not hasattr(user, "profile"):
            UserProfile.objects.create(user=user)


class Migration(migrations.Migration):
    dependencies = [
        ("cws2", "0005_add_admin_sheep_bot"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="profile",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "pronouns",
                    models.CharField(
                        blank=True,
                        help_text=(
                            "What pronouns should people use when referring to you?"
                        ),
                        max_length=64,
                        verbose_name="Pronouns",
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True,
                        help_text="Where in the world are you?",
                        max_length=64,
                        verbose_name="Location",
                    ),
                ),
                (
                    "bio",
                    models.TextField(
                        blank=True,
                        help_text=(
                            "Write something about yourself! This will appear on your"
                            " profile page."
                        ),
                        verbose_name="About me",
                    ),
                ),
            ],
        ),
        migrations.RunPython(
            generate_user_profiles,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
