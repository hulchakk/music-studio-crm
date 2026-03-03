import datetime
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError

from school.telegram_utils import send_telegram_msg


class Teacher(AbstractUser):
    telegram_id = models.CharField(
        max_length=55,
        null=True,
        unique=True,
        blank=True
    )
    phone_number = models.CharField(max_length=12, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["first_name", "last_name"],
                name="unique_teacher_constraint",
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    description = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["first_name", "last_name"],
                name="unique_student_constraint",
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Room(models.Model):
    name = models.CharField(max_length=55)
    description = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["name", "description"],
                name="unique_room_constraint",
            )
        ]

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
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            start = self.start_date
            self.end_date = start + datetime.timedelta(
                days=self.plan.validity_days
            )
        if self.lessons_left is None:
            self.lessons_left = self.plan.lessons_count

        if not self.pk:
            if self.teacher.telegram_id:
                text = (
                    f"🎉 <b>New Subscription!</b>\n\n"
                    f"👤 <b>Student:</b> {self.student}\n"
                    f"🎹 <b>Lessons:</b> {self.lessons_left}\n"
                    f"📅 <b>Expires:</b> {self.end_date.strftime('%d.%m.%Y') if self.end_date else 'No limit'}\n\n"
                    f"<i>Time to schedule some music!</i> 🎶"
                )
                send_telegram_msg(self.teacher.telegram_id, text)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.plan}"


class Lesson(models.Model):
    LESSON_STATUS = (
        ("planned", "Lesson is planned"),
        ("done", "Lesson is done"),
        ("skipped", "Lesson is skipped"),
    )
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
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=55, choices=LESSON_STATUS)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("start_datetime", )

    def clean(self):
        if self.subscription.lessons_left == 0 and not self.pk:
            raise ValidationError("No lessons left in this subscription")
        start_time = self.start_datetime
        self.end_datetime = start_time + datetime.timedelta(
            minutes=self.subscription.plan.lessons_duration
        )

        overlapping_lessons = Lesson.objects.filter(
                Q(start_datetime__lt=self.end_datetime) &
                Q(end_datetime__gt=self.start_datetime)
            )
        if self.pk:
            overlapping_lessons = overlapping_lessons.exclude(pk=self.pk)
        if overlapping_lessons.filter(room=self.room).exists():
            raise ValidationError(
                f"Room '{self.room}' is alredy booked for thi time"
            )
        if overlapping_lessons.filter(student=self.student).exists():
            raise ValidationError(
                f"Student {self.student} "
                "alredy have a lesson during this time"
            )
        if overlapping_lessons.filter(teacher=self.teacher).exists():
            raise ValidationError(
                f"Teacher {self.teacher} "
                "alredy have a lesson during this time"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.pk:
            if self.subscription.lessons_left > 0:
                self.subscription.lessons_left -= 1
                if self.subscription.lessons_left == 0:
                    self.subscription.is_active = False
                self.subscription.save()
        else:
            if self.teacher.telegram_id:
                text = (
                    f"<b>Lesson Updated!</b>\n\n"
                    f"Student: <b>{self.student}</b>\n"
                    f"📅 <b>New Time:</b> {self.start_datetime.strftime('%d.%m (%a) %H:%M')}\n"
                    f"📍 <b>Room:</b> {self.room}\n"
                    f"<i>Please check your schedule for any conflicts.</i>"
                )
                send_telegram_msg(self.teacher.telegram_id, text)
        super().save(*args, **kwargs)

    def __str__(self):
        start_time = self.start_datetime.strftime("%d.%m - %H:%M")
        return f"{self.student} ({self.teacher}) - {start_time}"
