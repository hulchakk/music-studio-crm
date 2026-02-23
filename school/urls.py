from django.urls import path

from school.views import (
    index,
    StudentsListView,
    TeacherListView,
    SubscriptionPlanListView,
    SubscriptionPlanDetailView,
    SubscriptionPlanCreateView,
    SubscriptionPlanUpdateView,
    SubscriptionPlabDeleteView,
)


urlpatterns = [
    path("", index, name="index"),
    path("students/", StudentsListView.as_view(), name="student-list"),
    path("teachers/", TeacherListView.as_view(), name="teacher-list"),
    path("plans/", SubscriptionPlanListView.as_view(), name="plan-list"),
    path(
        "plans/<int:pk>/",
        SubscriptionPlanDetailView.as_view(),
        name="plan-detail"
    ),
    path(
        "plans/create/",
        SubscriptionPlanCreateView.as_view(),
        name="plan-create"
    ),
    path(
        "plans/<int:pk>/update/",
        SubscriptionPlanUpdateView.as_view(),
        name="plan-update"
    ),
    path(
        "plans/<int:pk>/delete/",
        SubscriptionPlabDeleteView.as_view(),
        name="plan-delete"
    ),
]

app_name = "school"
