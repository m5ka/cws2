# Generated by Django 4.2.3 on 2023-10-12 08:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cws2", "0008_group_is_public_group_is_shared_group_owned_by"),
    ]

    operations = [
        migrations.CreateModel(
            name="Word",
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
                    "headword",
                    models.CharField(
                        db_index=True,
                        help_text="The word in your language. Double check you don't already have this word!",
                        max_length=255,
                        verbose_name="Word",
                    ),
                ),
                (
                    "alt_word",
                    models.CharField(
                        blank=True,
                        help_text="An alternative written form of this word. Useful if your language uses more than one script.",
                        max_length=255,
                        verbose_name="Alternative word",
                    ),
                ),
                (
                    "ipa",
                    models.CharField(
                        blank=True,
                        help_text="The pronunciation of this word in the International Phonetic Alphabet. Enter this as just IPA, without any enclosing brackets.",
                        max_length=255,
                        verbose_name="Pronunciation (IPA)",
                    ),
                ),
                (
                    "xsampa",
                    models.CharField(
                        blank=True,
                        help_text="The pronunciation of this word in X-SAMPA. Enter this as just X-SAMPA, without any enclosing brackets.",
                        max_length=255,
                        verbose_name="Pronunciation (X-SAMPA)",
                    ),
                ),
                (
                    "source_language",
                    models.CharField(
                        blank=True,
                        help_text="The language from which this word is derived or borrowed. Feel free to leave this blank, or use the 'etymology' field to give more detailed information.",
                        max_length=128,
                        verbose_name="Source language",
                    ),
                ),
                (
                    "etymology",
                    models.TextField(
                        blank=True,
                        help_text="An optional explanation of how this word came to be.",
                        verbose_name="Etymology",
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True,
                        help_text="Any other notes that might be useful for understanding this dictionary entry.",
                        verbose_name="Notes",
                    ),
                ),
                (
                    "reference_image",
                    models.CharField(
                        blank=True,
                        help_text="The URL of a reference image that can be displayed with the word summary. Useful for conscripts and sign-languages.",
                        max_length=255,
                        verbose_name="Image link",
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
                    "dialect",
                    models.ForeignKey(
                        blank=True,
                        help_text="If this word belongs to a specific dialect, you can set that here.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="words",
                        to="cws2.dialect",
                        verbose_name="Dialect",
                    ),
                ),
                (
                    "language",
                    models.ForeignKey(
                        help_text="The language to which is this word belongs.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="words",
                        to="cws2.language",
                        verbose_name="Language",
                    ),
                ),
                (
                    "roots",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Any words from which this word derives.",
                        to="cws2.word",
                        verbose_name="Roots",
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
            name="WordClass",
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
                    "label",
                    models.CharField(
                        help_text="The label for this word class, e.g. 'masculine' or 'imperfective'.",
                        max_length=64,
                        verbose_name="Label",
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
                        help_text="The language to which this word class belongs.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="classes",
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
            ],
        ),
        migrations.CreateModel(
            name="WordDefinition",
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
                    "part_of_speech",
                    models.CharField(
                        help_text="The part of speech for this definition of the word. If there's no exact match, just pick whichever is the closest.",
                        max_length=3,
                        verbose_name="Part of speech",
                    ),
                ),
                (
                    "register",
                    models.CharField(
                        blank=True,
                        help_text="Here you can optionally specify the social register of this word, i.e. what specific context does this word belong to?",
                        max_length=4,
                        verbose_name="Register",
                    ),
                ),
                (
                    "definition",
                    models.TextField(
                        help_text="If possible, keep this as succinct as possible. You can always add extra definitions to this word.",
                        verbose_name="Definition",
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
                    "classes",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Any classes to which this word belongs. If the classes have tables defined, these will be shown on the word's page.",
                        to="cws2.wordclass",
                        verbose_name="Classes",
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
                (
                    "word",
                    models.ForeignKey(
                        help_text="The word to which this definition belongs.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="definitions",
                        to="cws2.word",
                        verbose_name="Word",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="WordExample",
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
                    "text",
                    models.TextField(
                        help_text="This is the example containing this sense of the word.",
                        verbose_name="Example text",
                    ),
                ),
                (
                    "translation",
                    models.TextField(
                        blank=True,
                        help_text="Optionally, you can put the English translation of the example here.",
                        verbose_name="Example translation",
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
                    "definition",
                    models.ForeignKey(
                        help_text="The word definition to which this example belongs.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cws2.worddefinition",
                        verbose_name="Definition",
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
        migrations.AddConstraint(
            model_name="wordclass",
            constraint=models.UniqueConstraint(
                fields=("language", "label"), name="cws2_wordclass_language_label"
            ),
        ),
    ]
