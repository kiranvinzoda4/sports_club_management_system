# Generated by Django 4.0.1 on 2022-02-21 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0005_ground_ground_name_alter_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ground',
            name='ground_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sports',
            name='sports_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
