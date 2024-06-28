from rest_framework import serializers

from apps.profiles.models import User, CustomerProfile
from tools.django.django_tools import get_dynamic_attr


class AppProfileInformationGetSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar')
    bio = serializers.CharField(source='customer_profiles.first.bio', default=None)
    public = serializers.BooleanField(source='customer_profiles.first.public', default=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'bio', 'public']

    def get_avatar(self, obj):
        return get_dynamic_attr(obj, 'customer_profiles.get_dynamic_url')


class AppProfileInformationPostSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(default=None)
    last_name = serializers.CharField(default=None)
    username = serializers.CharField(required=True)

    class Meta:
        model = CustomerProfile
        fields = ['username', 'first_name', 'last_name', 'avatar', 'bio', 'public']
