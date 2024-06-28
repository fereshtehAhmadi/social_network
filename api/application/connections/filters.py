from django_filters import rest_framework

from apps.profiles.models import CustomerProfile


class CustomerProfilesFilter(rest_framework.FilterSet):
    username = rest_framework.CharFilter(method='user_name_filter')
    phone_number = rest_framework.CharFilter(method='phone_number_filter')

    class Meta:
        model = CustomerProfile
        fields = ["username", "phone_number"]

    def phone_number_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(user__phone_number=value)
        return queryset

    def user_name_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(user__username__icontains=value)
        return queryset
