# Generated by Django 4.0.1 on 2022-02-21 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0004_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='ground',
            name='ground_name',
            field=models.CharField(default='0000000', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
