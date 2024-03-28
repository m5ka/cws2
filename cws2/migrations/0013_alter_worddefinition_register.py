# Generated by Django 5.0.3 on 2024-03-28 18:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cws2", "0012_alter_worddefinition_part_of_speech"),
    ]

    operations = [
        migrations.AlterField(
            model_name="worddefinition",
            name="register",
            field=models.CharField(
                blank=True,
                choices=[
                    ("AFFC", "Affectionate/Endearing"),
                    ("ARCH", "Archaic"),
                    ("CASL", "Casual"),
                    ("DATD", "Dated"),
                    ("EUPH", "Euphemistic"),
                    ("FORM", "Formal/Polite"),
                    ("HONR", "Honorific"),
                    ("HUMB", "Humble"),
                    ("HMRS", "Humorous/Sarcastic"),
                    ("INTM", "Intimate"),
                    ("JRGN", "Jargon"),
                    ("POET", "Poetic"),
                    ("RELG", "Religious"),
                    ("SLNG", "Slang"),
                    ("TBOO", "Taboo"),
                    ("VULG", "Vulgar"),
                    ("OTHR", "Other (see notes)"),
                ],
                help_text="Here you can optionally specify the social register of this word, i.e. what specific context does this word belong to?",
                max_length=4,
                verbose_name="Register",
            ),
        ),
    ]
