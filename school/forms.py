from django import forms
from django.contrib.auth.forms import UserCreationForm

from school.models import (
    Student,
    SubscriptionPlan,
    Teacher,
)


class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


class TeacherCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Teacher
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "telegram_id",
            "description",
        )


class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            "username",
            "first_name",
            "last_name",
            "telegram_id",
            "phone_number",
            "description",
        ]
