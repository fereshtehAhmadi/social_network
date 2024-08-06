from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.application.search_users.filters import CustomerProfilesFilter
from api.application.search_users.serializers import AppUserListSerializer, AppUserProfileSerializer
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
    users_list="لیست کاربران",
    user_profile="صفحه کاربر",
)

tags = ['app_search_users_router/جستجو کاربران']
operationDescriptionsDict = dict()
get_swagger_kwargs = SwaggerAutoSchemaKwargs(
    manualParametersDict, operationDescriptionsDict, tags, operation_id
).get_kwargs


class AppSearchUsersAPI(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    serializers_dict = dict(
        GET=dict(
            users_list={
                "responses": {200: AppUserListSerializer},
            },
            user_profile={
                "responses": {200: AppUserProfileSerializer},
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
        serializer = AppUserProfileSerializer(customer, context={'user': request.user})
        return Response(serializer.data)

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
        customer = FactoryGetObject.find_object(CustomerProfile, pk=kwargs.get('pk'))
        serializer = AppUserProfileSerializer(customer)
        return Response(serializer.data)
