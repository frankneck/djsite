# Generated by Django 5.0.6 on 2024-06-13 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsite_app', '0003_alter_game_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='age',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
