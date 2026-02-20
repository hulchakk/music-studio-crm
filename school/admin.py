from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from school.models import (
    Lesson,
    Room,
    Student,
    Subscription,
    SubscriptionPlan,
    Teacher,
)


@admin.register(Teacher)
class TeacherAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "telegram_id",
        "phone_number",
        "description",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "telegram_id",
                        "phone_number",
                        "description",
                    )
                }
            )
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "telegram_id",
                        "phone_number",
                        "description",
                    )
                }
            )
        ),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "description",
    )


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "lessons_count",
        "price",
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "teacher",
        "plan",
        "lessons_left",
        "start_date",
        "end_date",
        "is_active",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "teacher",
        "room",
        "start_datetime",
        "status",
    )
