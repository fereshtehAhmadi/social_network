from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.application.connections.serializers import (
    AppRequestsListSerializer,
    AppConnectionListSerializer,
)
from apps.account.models import Connection
from apps.profiles.models import CustomerProfile

from tools.project.common.constants.cons import manualParametersDictCons
from tools.project.common.helper_func import FactoryGetObject
from tools.project.swagger_tools import SwaggerAutoSchemaKwargs

manualParametersDict = dict(
    default=[manualParametersDictCons.get("default")],
    users_list=[
        openapi.Parameter("username", in_=openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING, ),
        openapi.Parameter("phone_number", in_=openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING, ),
    ],
)

operation_id = dict(
    send_request="ارسال درخواست",
    requests_list="لیست درخواست ها",
    communicate="قبول درخواست",
    delete_connection="حذف ارتیاط",
    connection_list="لیست کاربران",
)

tags = ['connections/مدیریت درخواست ها']
operationDescriptionsDict = dict()
get_swagger_kwargs = SwaggerAutoSchemaKwargs(
    manualParametersDict, operationDescriptionsDict, tags, operation_id
).get_kwargs


class AppConnectionsAPI(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    serializers_dict = dict(
        GET=dict(
            send_request={
                "responses": {200: 'OK'},
            },
            requests_list={
                "responses": {200: AppRequestsListSerializer},
            },
            communicate={
                "responses": {200: 'OK'},
            },
            delete_connection={
                "responses": {200: 'OK'},
            },
            connection_list={
                "responses": {200: AppConnectionListSerializer},
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
            action_name="send_request",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=True)
    def send_request(self, request, **kwargs):
        """
        send follow request to other users
        if the person's page is public, the request will be approved by default
        and if it is private, it needs user approval.
        """
        connection = Connection.objects.filter(~Q(accepted=False),
                                               receiver__pk=kwargs.get('pk'),
                                               sender__user=request.user,
                                               is_active=True)
        if not connection.exists():
            sender = CustomerProfile.objects.get(user=request.user)
            receiver = CustomerProfile.objects.get(pk=kwargs.get('pk'))
            accepted = True if receiver.public else None
            Connection.objects.create(sender=sender, receiver=receiver, accepted=accepted)
        return Response('OK')

    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="GET",
            action_name="requests_list",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=False, url_path='requests/list')
    def requests_list(self, request, **kwargs):
        """
        accept follow request
        """
        connection = Connection.objects.filter(receiver__user=request.user, accepted__isnull=True, is_active=True)
        serializer = AppRequestsListSerializer(connection, context={'user': request.user}, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="GET",
            action_name="communicate",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=True)
    def communicate(self, request, **kwargs):
        """
        accept follow request
        """
        connection = FactoryGetObject.find_object(Connection, pk=kwargs.get('pk'), receiver__user=request.user,
                                                  accepted__isnull=True)
        connection.accepted = True
        connection.save()
        return Response('OK')

    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="GET",
            action_name="delete_connection",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=True)
    def delete_connection(self, request, **kwargs):
        """
        reject follow request or delete user to followers list
        """
        connection = FactoryGetObject.find_object(Connection, Q(sender__user=request.user) |
                                                  Q(receiver__user=request.user),
                                                  accepted__in=[True, None],
                                                  pk=kwargs.get('pk'))
        connection.is_active = False
        connection.save()
        return Response('OK')

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
        serializer = AppConnectionListSerializer(connection, context={'user': request.user}, many=True)
        return Response(serializer.data)
