from django.db.models import Q
from rest_framework import serializers

from apps.account.models import Connection
from apps.profiles.models import CustomerProfile
from tools.django.django_tools import get_dynamic_attr


class AppUserListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', ]

    def get_avatar(self, obj):
        return get_dynamic_attr(obj, 'get_dynamic_url')


class AppUserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    has_connection = serializers.SerializerMethodField('get_has_connection')

    class Meta:
        model = CustomerProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'public', 'has_connection', ]

    def get_avatar(self, obj):
        return get_dynamic_attr(obj, 'get_dynamic_url')

    def get_has_connection(self, obj):
        print(obj.user)
        print(self.context.get('user'))
        if obj.user == self.context.get('user'):
            return None
        connection = Connection.objects.filter(Q(sender=obj) | Q(receiver=obj))
        if connection.exists():
            return connection.first().accepted
        else:
            return False
