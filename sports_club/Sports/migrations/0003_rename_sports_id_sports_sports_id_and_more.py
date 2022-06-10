# Generated by Django 4.0.1 on 2022-02-12 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0002_sports'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sports',
            old_name='Sports_id',
            new_name='sports_id',
        ),
        migrations.RenameField(
            model_name='sports',
            old_name='Sports_name',
            new_name='sports_name',
        ),
        migrations.CreateModel(
            name='ground',
            fields=[
                ('ground_id', models.IntegerField(primary_key=True, serialize=False)),
                ('status', models.BooleanField()),
                ('sports_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sports.sports')),
            ],
        ),
    ]
