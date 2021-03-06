# Generated by Django 4.0.1 on 2022-02-10 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('mobile_no', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('address', models.CharField(max_length=200)),
                ('status', models.BooleanField()),
            ],
        ),
    ]
