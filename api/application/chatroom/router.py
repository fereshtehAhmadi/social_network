from rest_framework.routers import DefaultRouter

from api.application.chatroom.views import AppChatroomAPI

app_chatroom_router = DefaultRouter()

app_chatroom_router.register(prefix='', viewset=AppChatroomAPI, basename="chatroom")
