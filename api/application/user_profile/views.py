from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
