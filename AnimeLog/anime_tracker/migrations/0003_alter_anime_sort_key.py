# Generated by Django 4.1 on 2025-01-13 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime_tracker', '0002_anime_sort_key_anime_title_kana'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='sort_key',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
