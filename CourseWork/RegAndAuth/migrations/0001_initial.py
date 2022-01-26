# Generated by Django 4.0.1 on 2022-01-21 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Login', models.CharField(max_length=50, unique=True)),
                ('Password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserAndMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Login', models.CharField(max_length=50, unique=True)),
                ('EncryptMessage', models.CharField(default='Encrypted message', max_length=1000)),
            ],
        ),
    ]