# Generated by Django 4.0.1 on 2022-03-13 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0016_classes_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='tournament',
            fields=[
                ('tournament_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('details', models.CharField(default='0000000', max_length=100)),
                ('status', models.BooleanField()),
                ('sports', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sports.sports')),
                ('team_1', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='Sports.team')),
                ('team_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to='Sports.team')),
            ],
        ),
    ]