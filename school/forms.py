from django import forms

from school.models import (
    SubscriptionPlan,
)


class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"
