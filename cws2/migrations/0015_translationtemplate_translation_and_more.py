# Generated by Django 5.0.4 on 2024-04-26 18:55

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cws2", "0014_alter_word_uuid"),
    ]

    operations = [
        migrations.CreateModel(
            name="TranslationTemplate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("archived_at", models.DateTimeField(blank=True, null=True)),
                (
                    "uuid",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet=None,
                        db_index=True,
                        help_text="The unique ID for this translation.",
                        length=22,
                        max_length=22,
                        prefix="",
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="A short name for this translation.",
                        max_length=64,
                        verbose_name="Name",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="The text that should be translated.",
                        verbose_name="Text",
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        blank=True,
                        help_text="Where does this text come from?",
                        max_length=128,
                        verbose_name="Source",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="A description of the translation, giving some context or background.",
                        verbose_name="Description",
                    ),
                ),
                (
                    "archived_by",
                    models.ForeignKey(
                        blank=True,
                        db_column="archived_by_user_id",
                        db_index=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="archived_%(class)ss+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        db_column="created_by_user_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        db_column="updated_by_user_id",
                        db_index=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updated_%(class)ss+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Translation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("archived_at", models.DateTimeField(blank=True, null=True)),
                (
                    "translation",
                    models.TextField(
                        help_text="The translation of the text in your language.",
                        verbose_name="Translation",
                    ),
                ),
                (
                    "is_wip",
                    models.BooleanField(
                        default=False,
                        help_text="Is this translation a work in progress? If you tick yes, it won't be visible to anyone else.",
                        verbose_name="Work in progress",
                    ),
                ),
                (
                    "archived_by",
                    models.ForeignKey(
                        blank=True,
                        db_column="archived_by_user_id",
                        db_index=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="archived_%(class)ss+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        db_column="created_by_user_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "language",
                    models.ForeignKey(
                        help_text="The language this text is translated into.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="cws2.language",
                        verbose_name="Language",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        db_column="updated_by_user_id",
                        db_index=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updated_%(class)ss+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        db_column="translation_template_id",
                        help_text="The template of which this is a translation.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="cws2.translationtemplate",
                        verbose_name="Template",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="translation",
            constraint=models.UniqueConstraint(
                fields=("template", "language"),
                name="cws2_translation_unique_template_language",
            ),
        ),
    ]
