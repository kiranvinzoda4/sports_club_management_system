# Generated by Django 4.0.1 on 2022-03-12 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0015_classes'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes',
            name='details',
            field=models.CharField(default='0000000', max_length=100),
        ),
    ]
