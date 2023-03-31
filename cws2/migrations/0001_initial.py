# Generated by Django 4.1.7 on 2023-03-31 19:43

import cws2.models.base
import cws2.models.user
import cws2.validators
from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import re


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text=(
                            "Designates that this user has all permissions without"
                            " explicitly assigning them."
                        ),
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text=(
                            "Designates whether the user can log into this admin site."
                        ),
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text=(
                            "Designates whether this user should be treated as active."
                            " Unselect this instead of deleting accounts."
                        ),
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("uuid", models.CharField(db_index=True, max_length=22, unique=True)),
                (
                    "username",
                    models.CharField(
                        db_index=True,
                        help_text=(
                            "This is the unique identifier you'll use to log in. It"
                            " may only contain letters, numbers, hyphens, dashes and"
                            " dots."
                        ),
                        max_length=64,
                        unique=True,
                        validators=[
                            cws2.validators.validate_username_length,
                            django.core.validators.RegexValidator(
                                re.compile("^[a-zA-Z0-9-_.]+\\Z"),
                                (
                                    "Username may only contain letters, numbers,"
                                    " hyphens, underscores and dots."
                                ),
                                "invalid",
                            ),
                        ],
                        verbose_name="Username",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text=(
                            "This should be your email address. Make sure it's valid"
                            " and that you have access to it."
                        ),
                        max_length=128,
                        unique=True,
                        verbose_name="Email address",
                    ),
                ),
                ("email_confirmed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "display_name",
                    models.CharField(
                        blank=True,
                        help_text=(
                            "This name will appear instead of your username in some"
                            " places on the site, if set."
                        ),
                        max_length=64,
                        verbose_name="Display name",
                    ),
                ),
                (
                    "is_bot",
                    models.BooleanField(
                        default=False,
                        help_text=(
                            "If true, this user will be considered a staff-run bot"
                            " account and will not be able to be logged in to."
                        ),
                        verbose_name="Bot status",
                    ),
                ),
                (
                    "last_seen_ip",
                    models.CharField(
                        blank=True,
                        help_text="The last IP address this user used to log in.",
                        max_length=48,
                        verbose_name="Last seen IP",
                    ),
                ),
                (
                    "last_seen_route",
                    models.CharField(
                        blank=True,
                        help_text=(
                            "The route name of the last page this user accessed."
                        ),
                        max_length=64,
                        verbose_name="Last seen route",
                    ),
                ),
                (
                    "last_seen_at",
                    models.DateTimeField(
                        blank=True,
                        help_text="The last time this user accessed the site.",
                        null=True,
                        verbose_name="Last seen at",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text=(
                            "The groups this user belongs to. A user will get all"
                            " permissions granted to each of their groups."
                        ),
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            managers=[
                ("objects", cws2.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Group",
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
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="What should this group be called.",
                        max_length=64,
                        verbose_name="Name",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        help_text=(
                            "This is a unique group identifier that will appear in the"
                            " group's URL."
                        ),
                        max_length=64,
                        unique=True,
                        verbose_name="Identifier",
                    ),
                ),
                (
                    "icon",
                    models.CharField(
                        default="✱",
                        help_text=(
                            "A single character to represent the group in its icon."
                        ),
                        max_length=1,
                        verbose_name="Icon character",
                    ),
                ),
                (
                    "icon_colour_bg",
                    models.CharField(
                        default="#28A745",
                        help_text="The background colour of this group's icon.",
                        max_length=7,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^#[A-Fa-f0-9]{6}\\Z"),
                                "Colour is not a valid hexadecimal colour code.",
                                "invalid",
                            )
                        ],
                        verbose_name="Icon background colour",
                    ),
                ),
                (
                    "icon_colour_fg",
                    models.CharField(
                        default="#FFFFFF",
                        help_text="The foreground colour of this group's icon.",
                        max_length=7,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^#[A-Fa-f0-9]{6}\\Z"),
                                "Colour is not a valid hexadecimal colour code.",
                                "invalid",
                            )
                        ],
                        verbose_name="Icon foreground colour",
                    ),
                ),
                (
                    "access_type",
                    models.CharField(
                        choices=[
                            ("A", "Anyone"),
                            ("I", "Invite only"),
                            ("S", "System only"),
                        ],
                        help_text="Who should be allowed to join this group, and how?",
                        max_length=1,
                        verbose_name="Access type",
                    ),
                ),
                (
                    "is_hidden",
                    models.BooleanField(
                        default=False,
                        help_text=(
                            "Should this group be hidden from community group lists."
                        ),
                        verbose_name="Hidden status",
                    ),
                ),
                (
                    "is_everyone",
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        help_text=(
                            "Should all users automatically be part of this group?"
                        ),
                        verbose_name="Automatic-join status",
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
            bases=(cws2.models.base.AutoSlugMixin, models.Model),
        ),
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
        migrations.CreateModel(
            name="UserPermission",
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
                (
                    "ownable_model",
                    models.CharField(
                        help_text="The model name of the ownable resource.",
                        max_length=64,
                        verbose_name="Ownable model",
                    ),
                ),
                (
                    "ownable_pk",
                    models.BigIntegerField(
                        help_text="The unique ID of the ownable resource.",
                        verbose_name="Ownable ID",
                    ),
                ),
                (
                    "permissions",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=32),
                        blank=True,
                        default=list,
                        help_text="The permissions granted for this resource.",
                        size=None,
                        verbose_name="Permissions",
                    ),
                ),
                ("granted_at", models.DateTimeField(auto_now_add=True)),
                (
                    "granted_by",
                    models.ForeignKey(
                        db_column="granted_by_user_id",
                        db_index=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="granted_%(class)ss+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GroupPermission",
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
                (
                    "ownable_model",
                    models.CharField(
                        help_text="The model name of the ownable resource.",
                        max_length=64,
                        verbose_name="Ownable model",
                    ),
                ),
                (
                    "ownable_pk",
                    models.BigIntegerField(
                        help_text="The unique ID of the ownable resource.",
                        verbose_name="Ownable ID",
                    ),
                ),
                (
                    "permissions",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=32),
                        blank=True,
                        default=list,
                        help_text="The permissions granted for this resource.",
                        size=None,
                        verbose_name="Permissions",
                    ),
                ),
                ("granted_at", models.DateTimeField(auto_now_add=True)),
                (
                    "granted_by",
                    models.ForeignKey(
                        db_column="granted_by_user_id",
                        db_index=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="granted_%(class)ss+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="cws2.group",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GroupMembership",
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
                (
                    "permissions",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=32),
                        blank=True,
                        default=list,
                        help_text="The permissions this user has in the group.",
                        size=None,
                        verbose_name="Permissions in group",
                    ),
                ),
                ("joined_at", models.DateTimeField(auto_now_add=True)),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users",
                        to="cws2.group",
                    ),
                ),
                (
                    "invited_by",
                    models.ForeignKey(
                        db_column="invited_by_user_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memberships",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="userpermission",
            index=models.Index(
                fields=["ownable_model", "ownable_pk"],
                name="cws2_userpe_ownable_3092a8_idx",
            ),
        ),
        migrations.AddConstraint(
            model_name="userpermission",
            constraint=models.UniqueConstraint(
                fields=("ownable_model", "ownable_pk", "user"),
                name="cws2_userpermission_unique_model_pk_user",
            ),
        ),
        migrations.AddIndex(
            model_name="grouppermission",
            index=models.Index(
                fields=["ownable_model", "ownable_pk"],
                name="cws2_groupp_ownable_fd4dee_idx",
            ),
        ),
        migrations.AddConstraint(
            model_name="grouppermission",
            constraint=models.UniqueConstraint(
                fields=("ownable_model", "ownable_pk", "group"),
                name="cws2_grouppermission_unique_model_pk_user",
            ),
        ),
        migrations.AddConstraint(
            model_name="groupmembership",
            constraint=models.UniqueConstraint(
                fields=("group", "user"), name="cws2_groupmembership_group_user"
            ),
        ),
    ]
