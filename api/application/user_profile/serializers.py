from rest_framework import serializers

from apps.profiles.models import User


class AppUserInformationGetSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(
        source='customer_profiles.get_dynamic_url',
        default=None,
    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'avatar']
