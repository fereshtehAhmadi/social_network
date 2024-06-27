from django_filters import rest_framework

from apps.profiles.models import CustomerProfile


class CustomerProfilesFilter(rest_framework.FilterSet):
    slug = rest_framework.CharFilter(field_name="slug", lookup_expr="contains")
    phone_number = rest_framework.CharFilter(method='phone_number_filter')

    class Meta:
        model = CustomerProfile
        fields = ["slug", "phone_number"]

    def phone_number_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(user__phone_number=value)
        return queryset
