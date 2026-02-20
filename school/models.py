from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Teacher(AbstractBaseUser):
    telegram_id = models.CharField(max_length=55, null=True)
    phone_number = models.CharField(max_length=12)
    description = models.TextField(null=True)

class Student(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    description = models.TextField(null=True)

class Room(models.Model):
    name = models.CharField(max_length=55)
    description = models.TextField(null=True)
