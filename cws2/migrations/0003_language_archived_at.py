# Generated by Django 4.1.7 on 2023-03-26 19:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cws2", "0002_language"),
    ]

    operations = [
        migrations.AddField(
            model_name="language",
            name="archived_at",
            field=models.DateTimeField(null=True),
        ),
    ]