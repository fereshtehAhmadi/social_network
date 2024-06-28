from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.application.user_profile.serializers import (
    AppProfileInformationGetSerializer,
    AppProfileInformationPostSerializer,
)
from apps.profiles.models import CustomerProfile
from tools.project.common.constants.cons import manualParametersDictCons
from tools.project.swagger_tools import SwaggerAutoSchemaKwargs

manualParametersDict = dict(
    default=[manualParametersDictCons.get("default")],
)

operation_id = dict(
    profile_information_get="نمایش اطلاعات کاربر",
    profile_information_post="ارسال اطلاعات کاربر",
)

tags = ['profile/پروفایل']
operationDescriptionsDict = dict()
get_swagger_kwargs = SwaggerAutoSchemaKwargs(
    manualParametersDict, operationDescriptionsDict, tags, operation_id
).get_kwargs


class AppProfileAPI(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    serializers_dict = dict(
        GET=dict(
            profile_information_get={
                "responses": {200: AppProfileInformationGetSerializer},
            }
        ),
        POST=dict(
            profile_information_post={
                "request_body": AppProfileInformationPostSerializer,
                "responses": {200: "OK"},
            }
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
            action_name="profile_information_get",
            serializer=serializers_dict.get("GET"),
        )
    )
    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="POST",
            action_name="profile_information_post",
            serializer=serializers_dict.get("POST"),
        )
    )
    @action(methods=["GET", "POST"], detail=False, parser_classes=(FormParser, MultiPartParser))
    def profile_information(self, request, **kwargs):
        """
        display and update user information
        first_name, last_name, avatar
        """
        if request.method == 'POST':
            customer_profile = CustomerProfile.objects.filter(user=request.user).first()
            serializer = AppProfileInformationPostSerializer(instance=customer_profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            username = serializer.validated_data.pop('username')
            first_name = serializer.validated_data.pop('first_name')
            last_name = serializer.validated_data.pop('last_name')
            serializer.save()

            customer_profile.user.username = username
            customer_profile.user.first_name = first_name
            customer_profile.user.last_name = last_name
            customer_profile.user.save()
            return Response('OK')

        else:
            serializer = AppProfileInformationGetSerializer(request.user)
            return Response(serializer.data)
