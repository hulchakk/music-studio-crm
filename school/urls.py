from django.urls import path

from school.views import (
    index,
    StudentsView,
    TeacherView,
    SubscriptionPlanView,
    SubscriptionPlanDetailView,
)


urlpatterns = [
     path("", index, name="index"),
     path("students/", StudentsView.as_view(), name="student-list"),
     path("teachers/", TeacherView.as_view(), name="teacher-list"),
     path("plans/", SubscriptionPlanView.as_view(), name="plan-list"),
     path("plans/<int:pk>/", SubscriptionPlanDetailView.as_view(), name="plan-detail")
]

app_name = "school"
