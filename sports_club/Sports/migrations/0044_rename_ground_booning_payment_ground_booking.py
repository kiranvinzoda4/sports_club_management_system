# Generated by Django 4.0.1 on 2022-04-24 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0043_remove_payment_groung_payment_ground_booning'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='ground_booning',
            new_name='ground_booking',
        ),
    ]
