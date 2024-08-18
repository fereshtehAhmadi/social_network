from django.urls import re_path
from rest_framework.routers import DefaultRouter

from api.application.chatroom.views import AppChatroomAPI
from tools.project.websocket import consumer

app_chatroom_router = DefaultRouter()

app_chatroom_router.register(prefix='', viewset=AppChatroomAPI, basename="chatroom")

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumer.ChatConsumer.as_asgi()),
]
