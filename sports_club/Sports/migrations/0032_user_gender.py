# Generated by Django 4.0.1 on 2022-04-12 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0031_booking_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default='male', max_length=10),
        ),
    ]
