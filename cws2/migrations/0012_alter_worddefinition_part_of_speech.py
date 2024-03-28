# Generated by Django 5.0.3 on 2024-03-28 18:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cws2", "0011_group_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="worddefinition",
            name="part_of_speech",
            field=models.CharField(
                choices=[
                    ("ABB", "Abbreviation"),
                    ("ADJ", "Adjective"),
                    ("ADP", "Adposition"),
                    ("ADV", "Adverb"),
                    ("AFF", "Affix"),
                    ("AUX", "Auxiliary"),
                    ("C", "Conjunction"),
                    ("DET", "Determiner"),
                    ("I", "Interjection"),
                    ("N", "Noun"),
                    ("NUM", "Numeral"),
                    ("PTC", "Particle"),
                    ("PHR", "Phrase"),
                    ("P", "Pronoun"),
                    ("PPR", "Proper noun"),
                    ("V", "Verb"),
                ],
                help_text="The part of speech for this definition of the word. If there's no exact match, just pick whichever is the closest.",
                max_length=3,
                verbose_name="Part of speech",
            ),
        ),
    ]
