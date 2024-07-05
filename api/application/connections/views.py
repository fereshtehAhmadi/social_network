from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.application.connections.filters import CustomerProfilesFilter
from api.application.connections.serializers import AppUserListSerializer, AppUserProfileSerializer
from apps.account.models import Connection
from apps.profiles.models import CustomerProfile

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
    users_list="لیست کاربران",
    user_profile="صفحه کاربر",
    send_follow_request="ارسال درخواست دنبال کردن",
)

tags = ['connection/شبکه']
operationDescriptionsDict = dict()
get_swagger_kwargs = SwaggerAutoSchemaKwargs(
    manualParametersDict, operationDescriptionsDict, tags, operation_id
).get_kwargs


class AppConnectionsAPI(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    serializers_dict = dict(
        GET=dict(
            users_list={
                "responses": {200: AppUserListSerializer},
            },
            user_profile={
                "responses": {200: AppUserProfileSerializer},
            },
            send_follow_request={
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
            action_name="users_list",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=False, parser_classes=(FormParser, MultiPartParser))
    def users_list(self, request, **kwargs):
        """
        display users list

        """
        customers = CustomerProfilesFilter(request.GET).qs.filter(is_active=True).order_by('id').exclude(user=request.user)
        return Response(AppUserListSerializer(customers, many=True).data)

    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="GET",
            action_name="user_profile",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=True, parser_classes=(FormParser, MultiPartParser))
    def user_profile(self, request, **kwargs):
        """
        display selected user profile
        """
        customer = CustomerProfile.objects.get(pk=kwargs.get('pk'))
        serializer = AppUserProfileSerializer(customer)
        return Response(serializer.data)

    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="GET",
            action_name="send_follow_request",
            serializer=serializers_dict.get("GET"),
        )
    )
    @action(methods=["GET"], detail=True, parser_classes=(FormParser, MultiPartParser))
    def send_follow_request(self, request, **kwargs):
        """
        send follow request to other users
        if the person's page is public, the request will be approved by default
        and if it is private, it needs user approval.
        """
        connection = Connection.objects.filter(customer__pk=kwargs.get('pk'), connection__user=request.user)
        if not connection.exists():
            sender = CustomerProfile.objects.get(user=request.user)
            receiver = CustomerProfile.objects.get(pk=kwargs.get('pk'))
            accepted = True if receiver.public else None
            Connection.objects.create(connection=sender,
                                      customer=receiver, accepted=accepted)
        return Response('OK')
