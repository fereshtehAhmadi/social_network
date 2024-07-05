from rest_framework import serializers

from apps.account.models import Connection
from apps.profiles.models import CustomerProfile


class AppConnectionUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    avatar = serializers.SerializerMethodField('get_avatar', read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', ]


class AppRequestsListSerializer(serializers.ModelSerializer):
    connection = AppConnectionUserSerializer()

    class Meta:
        model = Connection
        fields = ['id', 'accepted', 'connection', ]
