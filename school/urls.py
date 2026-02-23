from django.urls import path

from school.views import (
    index,
    StudentsListView,
    TeacherListView,
    SubscriptionPlanListView,
    SubscriptionPlanDetailView,
)


urlpatterns = [
     path("", index, name="index"),
     path("students/", StudentsListView.as_view(), name="student-list"),
     path("teachers/", TeacherListView.as_view(), name="teacher-list"),
     path("plans/", SubscriptionPlanListView.as_view(), name="plan-list"),
     path("plans/<int:pk>/", SubscriptionPlanDetailView.as_view(), name="plan-detail")
]

app_name = "school"
