from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.application.chatroom.serializers import AppChatRoomSerializer, AppChatRoomConnectionsListSerializer

from apps.account.models import Connection
from apps.chatroom.models import ChatRoom

from tools.project.common.constants.cons import manualParametersDictCons
from tools.project.swagger_tools import SwaggerAutoSchemaKwargs

manualParametersDict = dict(
    default=[manualParametersDictCons.get("default")],
    users_list=[
        openapi.Parameter("username", in_=openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING, ),
        openapi.Parameter("phone_number", in_=openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING, ),
    ],
)

operation_id = dict(
    chatroom="لیست چت روم ها",
    connection_list="لیست کاربران",
)

tags = ['chatroom/چت روم']
operationDescriptionsDict = dict()
get_swagger_kwargs = SwaggerAutoSchemaKwargs(
    manualParametersDict, operationDescriptionsDict, tags, operation_id
).get_kwargs


class AppChatroomAPI(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    serializers_dict = dict(
        GET=dict(
            chatroom={
                "responses": {200: AppChatRoomSerializer},
            },
            connection_list={
                "responses": {200: AppChatRoomConnectionsListSerializer},
            },
        )
    )

    def get_serializer_class(self):
        return (
            self.serializers_dict.get(self.request.method)
            .get(self.action)
            .get("request_body")
        )

    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="GET",
            action_name="chatroom",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=False)
    def chatroom(self, request, **kwargs):
        """
        send follow request to other users
        if the person's page is public, the request will be approved by default
        and if it is private, it needs user approval.
        """
        chatroom = ChatRoom.objects.filter(Q(sender__user=request.user) | Q(receiver__user=request.user),
                                           is_active=True)
        serializer = AppChatRoomSerializer(chatroom, context={'user': request.user}, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="GET",
            action_name="connection_list",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=False, url_path='connection/list')
    def connection_list(self, request, **kwargs):
        """
        display following list
        """
        connection = Connection.objects.filter(Q(sender__user=request.user) | Q(receiver__user=request.user),
                                               accepted=True, is_active=True)
        serializer = AppChatRoomConnectionsListSerializer(connection, context={'user': request.user}, many=True)
        return Response(serializer.data)
