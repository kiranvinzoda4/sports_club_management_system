# Generated by Django 4.0.1 on 2022-03-11 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0012_remove_sports_no_of_player_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='sports',
        ),
    ]
