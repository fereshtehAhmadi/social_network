from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.application.user_profile.serializers import AppUserInformationGetSerializer
from tools.project.common.constants.cons import manualParametersDictCons
from tools.project.swagger_tools import SwaggerAutoSchemaKwargs

manualParametersDict = dict(
    default=[manualParametersDictCons.get("default")],
)

operation_id = dict(
    user_information_get="نمایش اطلاعات کاربر",
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
    @action(methods=["GET"], detail=False)
    def user_information(self, request, **kwargs):
        """
        display and update user information
        first_name, last_name, avatar
        """
        if request.method == 'GET':
            serializer = AppUserInformationGetSerializer(request.user)
            return Response(serializer.data)

        return Response("OK")
