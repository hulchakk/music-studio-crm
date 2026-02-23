from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from school.forms import (
    StudentForm,
    SubscriptionPlanForm,
    TeacherCreationForm,
    TeacherUpdateForm,
)
from school.models import (
    SubscriptionPlan,
    Teacher,
    Student,
    Lesson,
)


def index(request: HttpRequest) -> HttpResponse:
    teachers_count = Teacher.objects.count()
    students_count = Student.objects.count()
    lessons_count = Lesson.objects.count()
    context = {
        "teachers_count": teachers_count,
        "students_count": students_count,
        "lessons_count": lessons_count,
    }

    return render(request, "school/index.html", context=context)


class StudentListView(generic.ListView):
    model = Student


class StudentDetailView(generic.DetailView):
    model = Student


class StudentCreateView(generic.CreateView):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy("school:student-list")


class StudentUpdateView(generic.UpdateView):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy("school:student-list")


class StudentDeleteView(generic.DeleteView):
    model = Student
    success_url = reverse_lazy("school:student-list")


class TeacherListView(generic.ListView):
    model = Teacher


class TeacherDetailView(generic.DetailView):
    model = Teacher


class TeacherCreateView(generic.CreateView):
    model = Teacher
    form_class = TeacherCreationForm
    success_url = reverse_lazy("school:teacher-list")


class TeacherUpdateView(generic.UpdateView):
    model = Teacher
    form_class = TeacherUpdateForm
    success_url = reverse_lazy("school:teacher-list")


class TeacherDeleteView(generic.DeleteView):
    model = Teacher
    success_url = reverse_lazy("school:teacher-list")


class SubscriptionPlanListView(generic.ListView):
    model = SubscriptionPlan


class SubscriptionPlanDetailView(generic.DetailView):
    model = SubscriptionPlan


class SubscriptionPlanCreateView(generic.CreateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    success_url = reverse_lazy("school:plan-list")


class SubscriptionPlanUpdateView(generic.UpdateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    success_url = reverse_lazy("school:plan-list")


class SubscriptionPlabDeleteView(generic.DeleteView):
    model = SubscriptionPlan
    success_url = reverse_lazy("school:plan-list")
