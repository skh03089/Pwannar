# Generated by Django 2.0.1 on 2018-02-08 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0002_message_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='receiver_visibility',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='message',
            name='sender_visibility',
            field=models.BooleanField(default=True),
        ),
    ]
