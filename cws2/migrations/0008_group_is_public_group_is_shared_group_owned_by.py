# Generated by Django 4.2.3 on 2023-10-10 22:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cws2", "0007_language_language_flag"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="is_public",
            field=models.BooleanField(
                default=True,
                help_text="Does everyone have an implicit read permission for this resource?",
                verbose_name="Public status",
            ),
        ),
        migrations.AddField(
            model_name="group",
            name="is_shared",
            field=models.BooleanField(
                default=False,
                help_text="Are there specific user and group permissions set for this resource?",
                verbose_name="Sharing status",
            ),
        ),
        migrations.AddField(
            model_name="group",
            name="owned_by",
            field=models.ForeignKey(
                db_column="owned_by_user_id",
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="owned_%(class)ss",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
