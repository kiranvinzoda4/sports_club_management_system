# Generated by Django 4.0.1 on 2022-03-11 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0013_remove_player_sports'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='player',
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sports.team'),
        ),
    ]
