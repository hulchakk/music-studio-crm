from django.urls import path

from school.views import (
    index,
    StudentsView,
)


urlpatterns = [
     path("", index, name="index"),
     path("students/", StudentsView.as_view(), name="student-list")
]

app_name = "school"
