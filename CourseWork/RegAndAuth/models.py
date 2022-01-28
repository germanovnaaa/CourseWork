from django.db import models


class User(models.Model):
    Login = models.CharField(max_length=50, unique=True)
    Password = models.CharField(max_length=100)


class Message(models.Model):
    EncryptMessage = models.CharField(max_length=250, null=True)
    UserId = models.IntegerField(max_length=250, null=True)
