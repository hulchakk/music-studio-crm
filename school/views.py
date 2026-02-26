import datetime
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Value, CharField
from django.db.models.functions import Concat

from school.forms import (
    StudentForm,
    StudentSearchForm,
    SubscriptionCreationForm,
    SubscriptionUpdateForm,
    SubscriptionPlanForm,
    TeacherCreationForm,
    TeacherUpdateForm,
    TeacherSearchForm,
    SubsciptionFilterForm,
)
from school.models import (
    Subscription,
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
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        search_text = self.request.GET.get("search_text", "")
        context["search_form"] = StudentSearchForm(
            initial={
                "search_text": search_text,
            },
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_text = self.request.GET.get("search_text")
        if search_text:
            return queryset.annotate(
                full_name=Concat(
                    "first_name",
                    Value(" "),
                    "last_name",
                    output_field=CharField(),
                )
            ).filter(
                full_name__istartswith=search_text
            )

        return queryset


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
    paginate_by = 10

    def get_context_data(self):
        context = super(TeacherListView, self).get_context_data()
        search_text = self.request.GET.get("search_text", "")
        context["search_form"] = TeacherSearchForm(
            initial={
                "search_text": search_text,
            },
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_text = self.request.GET.get("search_text")
        if search_text:
            return queryset.annotate(
                full_name=Concat(
                    "first_name",
                    Value(" "),
                    "last_name",
                    output_field=CharField(),
                )
            ).filter(
                full_name__istartswith=search_text
            )

        return queryset


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
    paginate_by = 10


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


class SubscriptionsListView(generic.ListView):
    model = Subscription
    paginate_by = 10

    def get_context_data(self):
        context = super(SubscriptionsListView, self).get_context_data()

        filter_form = SubsciptionFilterForm(
            initial=self.request.GET
        )
        context["filter_form"] = filter_form

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.GET.get("student")
        teacher_id = self.request.GET.get("teacher")
        date_after = self.request.GET.get("date_after")
        date_before = self.request.GET.get("date_before")
        plan = self.request.GET.get("plan")

        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        if date_after:
            queryset = queryset.filter(
                start_date__gte=date_after,
            )
        if date_before:
            queryset = queryset.filter(
                start_date__lte=date_before,
            )
        if plan:
            queryset = queryset.filter(
                plan=plan
            )

        return queryset


class SubscriptionCreateView(generic.CreateView):
    model = Subscription
    form_class = SubscriptionCreationForm
    success_url = reverse_lazy("school:student-list")

    def get_initial(self):
        initial = super().get_initial()
        student_id = self.request.GET.get("student")
        teacher_id = self.request.GET.get("teacher")
        if student_id:
            initial["student"] = student_id
        if teacher_id:
            initial["teacher"] = teacher_id
        initial["start_date"] = datetime.date.today()
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        subscription = self.object
        schedule = {}

        for i in range(7):
            time_val = form.cleaned_data.get(f"time_{i}")
            if time_val:
                schedule[i] = time_val
        if not schedule:
            return response

        room = form.cleaned_data.get("room")
        current_date = subscription.start_date
        while subscription.lessons_left:
            week_day = current_date.weekday()
            if week_day in schedule:
                start_datetime = datetime.datetime.combine(
                    current_date,
                    schedule[week_day]
                )
                Lesson.objects.create(
                    student=subscription.student,
                    teacher=subscription.teacher,
                    subscription=subscription,
                    room=room,
                    start_datetime=start_datetime,
                    status="planned",
                )
            current_date += datetime.timedelta(days=1)

        return response


class SubscriptionUpdateView(generic.UpdateView):
    model = Subscription
    form_class = SubscriptionUpdateForm
    success_url = reverse_lazy("school:student-list")


class SubscriptionDeleteView(generic.DeleteView):
    model = Subscription
    success_url = reverse_lazy("school:student-list")
