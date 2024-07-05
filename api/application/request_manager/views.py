from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.application.request_manager.serializers import (
    AppRequestsListSerializer,
    AppFollowersListSerializer,
    AppFollowingListSerializer,
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
    send_follow_request="ارسال درخواست دنبال کردن",
    requests_list="لیست درخواست ها",
    accept_follow_request="قبول درخواست",
    reject_follow_request="رد درخواست/ حذف فالوور",
    followers_list="لیست دنبال کنندگان",
    following_list="لیست دنبال شوندگان",
    unfollow="لغو دنبال کردن",
)

tags = ['request_manager/مدیریت درخواست ها']
operationDescriptionsDict = dict()
get_swagger_kwargs = SwaggerAutoSchemaKwargs(
    manualParametersDict, operationDescriptionsDict, tags, operation_id
).get_kwargs


class AppRequestManagerAPI(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    serializers_dict = dict(
        GET=dict(
            send_follow_request={
                "responses": {200: 'OK'},
            },
            requests_list={
                "responses": {200: AppRequestsListSerializer},
            },
            accept_follow_request={
                "responses": {200: 'OK'},
            },
            reject_follow_request={
                "responses": {200: 'OK'},
            },
            followers_list={
                "responses": {200: AppFollowersListSerializer},
            },
            following_list={
                "responses": {200: AppFollowingListSerializer},
            },
            unfollow={
                "responses": {200: 'OK'},
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
            action_name="send_follow_request",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=True)
    def send_follow_request(self, request, **kwargs):
        """
        send follow request to other users
        if the person's page is public, the request will be approved by default
        and if it is private, it needs user approval.
        """
        connection = Connection.objects.filter(~Q(accepted=False),
                                               customer__pk=kwargs.get('pk'),
                                               connection__user=request.user,
                                               is_active=True)
        if not connection.exists():
            sender = CustomerProfile.objects.get(user=request.user)
            receiver = CustomerProfile.objects.get(pk=kwargs.get('pk'))
            accepted = True if receiver.public else None
            Connection.objects.create(connection=sender,
                                      customer=receiver, accepted=accepted)
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
        connection = Connection.objects.filter(customer__user=request.user, accepted__isnull=True, is_active=True)
        serializer = AppRequestsListSerializer(connection, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="GET",
            action_name="accept_follow_request",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=True)
    def accept_follow_request(self, request, **kwargs):
        """
        accept follow request
        """
        connection = FactoryGetObject.find_object(Connection, pk=kwargs.get('pk'), customer__user=request.user,
                                                  accepted__isnull=True)
        connection.accepted = True
        connection.save()
        return Response('OK')

    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="GET",
            action_name="reject_follow_request",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=True)
    def reject_follow_request(self, request, **kwargs):
        """
        reject follow request or delete user to followers list
        """
        connection = FactoryGetObject.find_object(Connection, pk=kwargs.get('pk'), customer__user=request.user,
                                                  accepted__in=[True, None])
        connection.accepted = False
        connection.save()
        return Response('OK')

    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="GET",
            action_name="followers_list",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=False, url_path='followers/list')
    def followers_list(self, request, **kwargs):
        """
        display followers list
        """
        connection = Connection.objects.filter(customer__user=request.user, accepted=True, is_active=True)
        serializer = AppFollowersListSerializer(connection, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="GET",
            action_name="following_list",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=False, url_path='following/list')
    def following_list(self, request, **kwargs):
        """
        display following list
        """
        connection = Connection.objects.filter(connection__user=request.user, accepted=True, is_active=True)
        serializer = AppFollowingListSerializer(connection, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="GET",
            action_name="unfollow",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=False, url_path='following/list')
    def unfollow(self, request, **kwargs):
        """
        unfollow action
        """
        connection = FactoryGetObject.find_object(Connection, pk=kwargs.get('pk'), accepted=True,
                                                  connection__user=request.user, is_active=True)
        connection.accepted = False
        return Response('OK')
