from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Teacher(AbstractBaseUser):
    telegram_id = models.CharField(max_length=55, null=True, unique=True)
    phone_number = models.CharField(max_length=12, unique=True)
    description = models.TextField(null=True)


class Student(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    description = models.TextField(null=True)


class Room(models.Model):
    name = models.CharField(max_length=55, unique=True)
    description = models.TextField(null=True)


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255, unique=True)
    lessons_count = models.IntegerField()
    lessons_duration = models.IntegerField()
    price = models.IntegerField()
    validity_days = models.IntegerField()


class Subscription(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    lessons_left = models.IntegerField()
    is_active = models.BooleanField(default=False)


class Lesson(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=55)
    notes = models.TextField()
