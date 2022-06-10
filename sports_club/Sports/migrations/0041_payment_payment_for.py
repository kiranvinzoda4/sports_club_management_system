# Generated by Django 4.0.1 on 2022-04-24 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0040_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_for',
            field=models.IntegerField(choices=[(1, 'GROUND BOOKING'), (2, 'FOR CLASS')], default=1),
        ),
    ]