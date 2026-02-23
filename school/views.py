from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from school.models import (
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


class StudentsView(generic.ListView):
    model = Student


class TeacherView(generic.ListView):
    model = Teacher
