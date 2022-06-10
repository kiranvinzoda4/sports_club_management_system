# Generated by Django 4.0.1 on 2022-03-13 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0017_tournament'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='date',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='time',
        ),
        migrations.AddField(
            model_name='tournament',
            name='booking',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sports.booking'),
        ),
    ]
