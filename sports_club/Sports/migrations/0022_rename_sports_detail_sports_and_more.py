# Generated by Django 4.0.1 on 2022-03-22 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0021_rename_sports_sports_detail_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='sports_detail',
            new_name='sports',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='sports_detail',
            new_name='sports',
        ),
        migrations.RenameField(
            model_name='classes',
            old_name='sports_detail',
            new_name='sports',
        ),
        migrations.RenameField(
            model_name='ground',
            old_name='sports_detail',
            new_name='sports',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='sports_detail',
            new_name='sports',
        ),
        migrations.RenameField(
            model_name='tournament',
            old_name='sports_detail',
            new_name='sports',
        ),
    ]
