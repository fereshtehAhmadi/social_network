from docutils.transforms.universal import Messages
from rest_framework import serializers

from apps.account.models import Connection
from apps.chatroom.models import ChatRoom, Message
from apps.profiles.models import CustomerProfile
from tools.django.dynamic_attr import get_dynamic_attr


class AppChatRoomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    avatar = serializers.SerializerMethodField('get_avatar', read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', ]

    def get_avatar(self, obj):
        return get_dynamic_attr(obj, 'get_dynamic_url')


class AppChatRoomSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = ChatRoom
        fields = ['id', 'user', 'new_messages', ]

    def get_user(self, obj):
        if obj.sender.user == self.context.get('user'):
            return AppChatRoomUserSerializer(obj.receiver).data
        else:
            return AppChatRoomUserSerializer(obj.sender).data


class AppChatRoomConnectionsListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = Connection
        fields = ['id', 'accepted', 'user', ]

    def get_user(self, obj):
        if obj.sender.user == self.context.get('user'):
            return AppChatRoomUserSerializer(obj.receiver).data
        else:
            return AppChatRoomUserSerializer(obj.sender).data


class AppMessagesListSerializer(serializers.ModelSerializer):
    is_sender = serializers.SerializerMethodField('get_is_sender')
    file_message = serializers.CharField(source='get_dynamic_url')

    class Meta:
        model = Message
        fields = ['id', 'message', 'file_message', 'is_sender', 'seen', ]

    def get_is_sender(self, obj):
        print('********************')
        print(obj.sender)
        print(obj.sender.user)
        print(self.context.get('user'))
        if obj.sender.user == self.context.get('user'):
            return True
        else:
            return False


class AppSendMessageInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['receiver', 'message', 'file_message', ]
