# Generated by Django 4.2.3 on 2023-09-17 14:14

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cws2", "0003_add_groups_bots"),
    ]

    operations = [
        migrations.CreateModel(
            name="PhonoSystem",
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
                    "is_public",
                    models.BooleanField(
                        default=True,
                        help_text="Does everyone have an implicit read permission for this resource?",
                        verbose_name="Public status",
                    ),
                ),
                (
                    "is_shared",
                    models.BooleanField(
                        default=False,
                        help_text="Are there specific user and group permissions set for this resource?",
                        verbose_name="Sharing status",
                    ),
                ),
                ("uuid", models.CharField(db_index=True, max_length=22, unique=True)),
                (
                    "is_human",
                    models.CharField(
                        db_index=True,
                        default=False,
                        help_text="Indicates whether this is the Human Phono System.",
                        verbose_name="Default human phono system",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="This is the name of the phono system.",
                        max_length=64,
                        verbose_name="Name",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("D", "Draft"), ("P", "Published")],
                        default="D",
                        help_text="This is the status of the phono system.",
                        max_length=1,
                        verbose_name="Phono system status",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="This is a brief summary explaining the context of the phono system.",
                        verbose_name="Summary",
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
                    "owned_by",
                    models.ForeignKey(
                        db_column="owned_by_user_id",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="owned_%(class)ss",
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
            name="Phone",
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
                ("uuid", models.CharField(db_index=True, max_length=22, unique=True)),
                (
                    "glyph",
                    models.CharField(
                        help_text="This is a glyph that represents the phone.",
                        max_length=12,
                        verbose_name="Glyph",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="This is the name of the phone.",
                        max_length=64,
                        verbose_name="Name",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("C", "Consonant"),
                            ("V", "Vowel"),
                            ("Q", "Quality"),
                            ("U", "Uncategorized"),
                        ],
                        help_text="This is the category of the phone.",
                        max_length=1,
                        verbose_name="Category",
                    ),
                ),
                (
                    "ipa",
                    models.CharField(
                        help_text="This is the IPA phonetic representation of this phone.",
                        max_length=12,
                        verbose_name="IPA",
                    ),
                ),
                (
                    "xsampa",
                    models.CharField(
                        help_text="This is the X-Sampa phonetic representation of this phone.",
                        max_length=12,
                        blank=True,
                        verbose_name="X-Sampa",
                    ),
                ),
                (
                    "tags",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=32),
                        blank=True,
                        default=list,
                        help_text="Tags associated with this phone.",
                        size=None,
                        verbose_name="Tags",
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
                    "phono_system",
                    models.ForeignKey(
                        db_column="phono_system_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cws2.phonosystem",
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
        ),
        migrations.AddConstraint(
            model_name="phone",
            constraint=models.UniqueConstraint(
                fields=("phono_system_id", "glyph", "category"),
                name="cws2_phone_unique_phono_system_glyph_category",
            ),
        ),
    ]
