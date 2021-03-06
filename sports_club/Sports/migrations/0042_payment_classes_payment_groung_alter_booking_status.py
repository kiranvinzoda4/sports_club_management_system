# Generated by Django 4.0.1 on 2022-04-24 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0041_payment_payment_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='classes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Sports.classes'),
        ),
        migrations.AddField(
            model_name='payment',
            name='groung',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Sports.ground'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
