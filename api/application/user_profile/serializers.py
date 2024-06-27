from rest_framework import serializers

from apps.profiles.models import User, CustomerProfile
from tools.django.django_tools import get_dynamic_attr


class AppProfileInformationGetSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar')
    bio = serializers.CharField(source='customer_profiles.first.bio', default=None)
    slug = serializers.CharField(source='customer_profiles.first.slug', default=None)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'avatar', 'bio', 'slug']

    def get_avatar(self, obj):
        return get_dynamic_attr(obj, 'customer_profiles.get_dynamic_url')


class AppProfileInformationPostSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(default=None)
    last_name = serializers.CharField(default=None)

    class Meta:
        model = CustomerProfile
        fields = ['first_name', 'last_name', 'avatar', 'bio', 'slug', ]
