from rest_framework import serializers

from apps.profiles.models import User
from tools.django.django_tools import get_dynamic_attr


class AppUserInformationGetSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'avatar']

    def get_avatar(self, obj):
        return get_dynamic_attr(obj, 'customer_profiles.get_dynamic_url')


class AppUserInformationPostSerializer(serializers.ModelSerializer):
    avatar = serializers.FileField(allow_null=True, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', ]
