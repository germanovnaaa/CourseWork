# Generated by Django 4.0.1 on 2022-01-22 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RegAndAuth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EncryptMessage', models.CharField(max_length=1000, null=True)),
                ('Mess', models.CharField(max_length=1000, null=True)),
                ('Username', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Person',
            new_name='User',
        ),
        migrations.DeleteModel(
            name='UserAndMessage',
        ),
    ]
