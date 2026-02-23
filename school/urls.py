from django.urls import path

from school.views import (
    index,
    StudentsView,
    TeacherView,
)


urlpatterns = [
     path("", index, name="index"),
     path("students/", StudentsView.as_view(), name="student-list"),
     path("teachers/", TeacherView.as_view(), name="teacher-list"),
]

app_name = "school"
