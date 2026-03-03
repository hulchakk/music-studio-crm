import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from school.forms import (
    LessonForm,
    StudentForm,
    StudentSearchForm,
    SubscriptionCreationForm,
    SubscriptionUpdateForm,
    SubscriptionPlanForm,
    TeacherCreationForm,
    TeacherUpdateForm,
    TeacherSearchForm,
    SubsciptionFilterForm,
    ScheduleFilterForm,
    MyScheduleFilterForm,
)
from school.models import (
    Subscription,
    SubscriptionPlan,
    Teacher,
    Student,
    Lesson,
)


@login_required
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


@login_required
def schedule(request: HttpRequest) -> HttpResponse:
    if not request.user.is_superuser:
        raise PermissionDenied
    today = datetime.date.today()
    form_data = request.GET.copy()
    queryset = None
    week = form_data.get("week")
    if not week:
        year, week_num, _ = today.isocalendar()
        form_data["week"] = f"{year}-W{week_num:02d}"
        week = form_data["week"]

    filter_form = ScheduleFilterForm(
        data=form_data,
    )

    if filter_form.is_valid():
        queryset = Lesson.objects.all()
        filters = filter_form.cleaned_data
        teacher = filters.get("teacher")
        student = filters.get("student")
        room = filters.get("room")

        if teacher:
            queryset = queryset.filter(
                teacher_id=teacher,
            )
        if student:
            queryset = queryset.filter(
                student_id=student,
            )
        if room:
            queryset = queryset.filter(
                room_id=room,
            )

    week_start_date = datetime.datetime.strptime(
        week + "-1",
        "%G-W%V-%u"
    ).date()
    context = {
        "filter_form": filter_form,
        "week_days": [],
    }
    for week_day in range(7):
        day_date = week_start_date + datetime.timedelta(days=week_day)
        if queryset:
            day_lessons = queryset.filter(
                        start_datetime__date=day_date,
            )
        else:
            day_lessons = []
        context["week_days"].append(
            {
                "name": day_date.strftime("%A"),
                "date": day_date,
                "lessons": day_lessons,
            },
        )

    return render(request, "school/schedule.html", context=context)


class StudentListView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.ListView
):
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

    def test_func(self):
        return self.request.user.is_superuser


class StudentDetailView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DetailView
):
    model = Student

    def test_func(self):
        return self.request.user.is_superuser


class StudentCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.CreateView
):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy("school:student-list")

    def test_func(self):
        return self.request.user.is_superuser


class StudentUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy("school:student-list")

    def test_func(self):
        return self.request.user.is_superuser


class StudentDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = Student
    success_url = reverse_lazy("school:student-list")

    def test_func(self):
        return self.request.user.is_superuser


class TeacherListView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.ListView
):
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

    def test_func(self):
        return self.request.user.is_superuser


class TeacherDetailView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DetailView
):
    model = Teacher

    def test_func(self):
        return self.request.user.is_superuser


class TeacherCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.CreateView
):
    model = Teacher
    form_class = TeacherCreationForm
    success_url = reverse_lazy("school:teacher-list")

    def test_func(self):
        return self.request.user.is_superuser


class TeacherUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = Teacher
    form_class = TeacherUpdateForm
    success_url = reverse_lazy("school:teacher-list")

    def test_func(self):
        return self.request.user.is_superuser


class TeacherDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = Teacher
    success_url = reverse_lazy("school:teacher-list")

    def test_func(self):
        return self.request.user.is_superuser


class SubscriptionPlanListView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.ListView
):
    model = SubscriptionPlan
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_superuser


class SubscriptionPlanDetailView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DetailView
):
    model = SubscriptionPlan

    def test_func(self):
        return self.request.user.is_superuser


class SubscriptionPlanCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.CreateView
):
    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    success_url = reverse_lazy("school:plan-list")

    def test_func(self):
        return self.request.user.is_superuser


class SubscriptionPlanUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    success_url = reverse_lazy("school:plan-list")

    def test_func(self):
        return self.request.user.is_superuser


class SubscriptionPlabDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = SubscriptionPlan
    success_url = reverse_lazy("school:plan-list")

    def test_func(self):
        return self.request.user.is_superuser


class SubscriptionsListView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.ListView
):
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

    def test_func(self):
        return self.request.user.is_superuser


class SubscriptionCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.CreateView
):
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

    def test_func(self):
        return self.request.user.is_superuser


class SubscriptionUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = Subscription
    form_class = SubscriptionUpdateForm
    success_url = reverse_lazy("school:student-list")

    def test_func(self):
        return self.request.user.is_superuser


class SubscriptionDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = Subscription
    success_url = reverse_lazy("school:student-list")

    def test_func(self):
        return self.request.user.is_superuser


class LessonUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = Lesson
    form_class = LessonForm
    success_url = reverse_lazy("school:schedule")

    def test_func(self):
        return (self.request.user.is_superuser) or (
            self.request.user.pk == self.get_object().teacher.pk
        )


class LessonCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.CreateView
):
    model = Lesson
    form_class = LessonForm
    success_url = reverse_lazy("school:schedule")

    def get_initial(self):
        initial = super().get_initial()
        initial.update(self.request.GET.dict())
        initial["status"] = "planned"
        return initial

    def test_func(self):
        return self.request.user.is_superuser


class MyProfileView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DetailView
):
    model = Teacher
    template_name = "school/profile.html"

    def test_func(self):
        return (
            self.request.user.pk == self.kwargs.get("pk")
        ) or self.request.user.is_superuser


@login_required
def my_schedule(request: HttpRequest, pk) -> HttpResponse:
    if request.user.pk != pk:
        raise PermissionDenied
    today = datetime.date.today()
    form_data = request.GET.copy()
    queryset = Lesson.objects.filter(
            teacher_id=pk
        )
    week = form_data.get("week")
    if not week:
        year, week_num, _ = today.isocalendar()
        form_data["week"] = f"{year}-W{week_num:02d}"
        week = form_data["week"]

    filter_form = MyScheduleFilterForm(
        data=form_data,
    )

    if filter_form.is_valid():
        filters = filter_form.cleaned_data
        student = filters.get("student")
        room = filters.get("room")
        if student:
            queryset = queryset.filter(
                student_id=student,
            )
        if room:
            queryset = queryset.filter(
                room_id=room,
            )

    week_start_date = datetime.datetime.strptime(
        week + "-1",
        "%G-W%V-%u"
    ).date()
    context = {
        "filter_form": filter_form,
        "week_days": [],
    }
    for week_day in range(7):
        day_date = week_start_date + datetime.timedelta(days=week_day)
        if queryset:
            day_lessons = queryset.filter(
                        start_datetime__date=day_date,
            )
        else:
            day_lessons = []
        context["week_days"].append(
            {
                "name": day_date.strftime("%A"),
                "date": day_date,
                "lessons": day_lessons,
            },
        )

    return render(request, "school/my_schedule.html", context=context)
