from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from school.forms import SubscriptionPlanForm
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


class StudentsListView(generic.ListView):
    model = Student


class TeacherListView(generic.ListView):
    model = Teacher


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
