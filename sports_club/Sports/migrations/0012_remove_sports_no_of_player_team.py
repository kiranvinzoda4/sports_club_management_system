# Generated by Django 4.0.1 on 2022-03-11 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0011_remove_player_status_player_sports'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sports',
            name='no_of_player',
        ),
        migrations.CreateModel(
            name='team',
            fields=[
                ('team_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='0000000', max_length=100)),
                ('player', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sports.player')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sports.user')),
            ],
        ),
    ]
