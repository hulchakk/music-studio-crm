from django import forms
from django.contrib.auth.forms import UserCreationForm

from school.models import (
    Room,
    Student,
    Subscription,
    SubscriptionPlan,
    Teacher,
)


class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"


class SubscriptionCreationForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
    )
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        required=False,
        label="Room to fill up schedule",
    )
    for i, day_name in [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]:
        locals()[f"time_{i}"] = forms.TimeField(
            widget=forms.TimeInput(attrs={"type": "time"}),
            required=False,
            label=f"{day_name} at"
        )

    class Meta:
        model = Subscription
        fields = (
            "student",
            "teacher",
            "plan",
            "start_date",
        )

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get("room")
        has_schedule = any(cleaned_data.get(f"time_{i}") for i in range(7))
        if has_schedule and not room:
            self.add_error("room", "Please choose room for schedule")

        return cleaned_data


class SubscriptionUpdateForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
    )

    class Meta:
        model = Subscription
        fields = (
            "student",
            "teacher",
            "start_date",
            "end_date",
            "lessons_left",
        )


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


class StudentSearchForm(forms.Form):
    search_text = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search student"
            }
        )
    )


class TeacherCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Teacher
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "phone_number",
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


class TeacherSearchForm(forms.Form):
    search_text = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search teacher"
            }
        )
    )


class SubsciptionFilterForm(forms.Form):
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        required=False,
    )
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        required=False,
    )
    date_before = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
    )
    date_after = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
    )
    plan = forms.ModelChoiceField(
        queryset=SubscriptionPlan.objects.all(),
        required=False,
    )
