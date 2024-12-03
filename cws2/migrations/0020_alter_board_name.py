# Generated by Django 5.1.3 on 2024-11-29 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cws2', '0019_add_default_boards'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='name',
            field=models.CharField(db_index=True, help_text='What should this board be called? This will appear in the boards page.', max_length=64, verbose_name='Name'),
        ),
    ]