import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class Teacher(AbstractUser):
    telegram_id = models.CharField(max_length=55, null=True, unique=True, blank=True)
    phone_number = models.CharField(max_length=12, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Room(models.Model):
    name = models.CharField(max_length=55, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.description[:10]}..."


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255, unique=True)
    lessons_count = models.IntegerField()
    lessons_duration = models.IntegerField()
    price = models.IntegerField()
    validity_days = models.IntegerField()

    def __str__(self):
        return self.name


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
    start_date = models.DateField()
    end_date = models.DateField(
        null=True,
        blank=True,
    )
    lessons_left = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.end_date:
            start = self.start_date
            self.end_date = start + datetime.timedelta(days=self.plan.validity_days)
        if not self.lessons_left:
            self.lessons_left = self.plan.lessons_count
        super().save(*args, **kwargs)


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
    end_datetime = models.DateTimeField(
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=55)
    notes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.end_datetime:
            start_time = self.start_datetime
            self.end_datetime = start_time + datetime.timedelta(minutes=self.plan.lessons_duration)
        super().save(*args, **kwargs)
