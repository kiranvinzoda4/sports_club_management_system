# Generated by Django 4.0.1 on 2022-04-19 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sports', '0034_user_forgot_pass_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='forgot_pass_token',
            new_name='email_token',
        ),
    ]
