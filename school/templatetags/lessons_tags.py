from django import template


register = template.Library()


@register.filter
def count_planned(queryset):
    return queryset.filter(status="planned").count()
