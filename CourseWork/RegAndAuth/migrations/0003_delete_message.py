# Generated by Django 4.0.1 on 2022-01-24 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RegAndAuth', '0002_message_rename_person_user_delete_userandmessage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]
