from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.application.user_profile.serializers import AppUserInformationGetSerializer, AppUserInformationPostSerializer
from apps.profiles.models import CustomerProfile
from tools.project.common.constants.cons import manualParametersDictCons
from tools.project.swagger_tools import SwaggerAutoSchemaKwargs

manualParametersDict = dict(
    default=[manualParametersDictCons.get("default")],
)

operation_id = dict(
    user_information_get="نمایش اطلاعات کاربر",
    user_information_post="ارسال اطلاعات کاربر",
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
            user_information_get={
                "responses": {200: AppUserInformationGetSerializer},
            }
        ),
        POST=dict(
            user_information_post={
                "request_body": AppUserInformationPostSerializer,
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
            action_name="user_information_get",
            serializer=serializers_dict.get("GET"),
        )
    )
    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="POST",
            action_name="user_information_post",
            serializer=serializers_dict.get("POST"),
        )
    )
    @action(methods=["GET", "POST"], detail=False, parser_classes=(FormParser, MultiPartParser))
    def user_information(self, request, **kwargs):
        """
        display and update user information
        first_name, last_name, avatar
        """
        if request.method == 'POST':
            customer_profile = CustomerProfile.objects.filter(user=request.user).first()
            serializer = AppUserInformationPostSerializer(instance=request.user, data=request.data)
            serializer.is_valid(raise_exception=True)
            avatar = serializer.validated_data.pop('avatar', None)
            serializer.save()

            customer_profile.avatar = avatar
            customer_profile.save()

        else:
            serializer = AppUserInformationGetSerializer(request.user)
            return Response(serializer.data)

        return Response("OK")
