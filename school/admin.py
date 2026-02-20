from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from school.models import (
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
