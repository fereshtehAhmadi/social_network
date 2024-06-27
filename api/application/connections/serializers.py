from rest_framework import serializers

from apps.profiles.models import CustomerProfile
from tools.django.django_tools import get_dynamic_attr


class AppUserListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['id', 'first_name', 'last_name', 'slug', 'phone_number', 'avatar', ]

    def get_avatar(self, obj):
        return get_dynamic_attr(obj, 'get_dynamic_url')
