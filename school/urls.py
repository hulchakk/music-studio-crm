from django.urls import path

from school.views import (
    index,
)


urlpatterns = [
     path("", index, name="index"),
]

app_name = "school"
