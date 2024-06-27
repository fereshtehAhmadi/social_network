import uuid

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rolepermissions.checkers import has_role
from rolepermissions.roles import assign_role

from api.application.verification.serializers import (
    AppLoginCreateOtpSerializer,
    AppLoginValidateOtpSerializer,
    AppLoginCreateTokenSerializer, AppUserInformationPostSerializer, AppUserInformationGetSerializer,
)
from apps.profiles.models import CustomerProfile, User
from tools.project.common.constants.cons import manualParametersDictCons
from tools.project.common.constants.model_cons import UserRoleChoice
from tools.project.sms.service import SmsCreatorService
from tools.project.swagger_tools import SwaggerAutoSchemaKwargs
from tools.project.verification_serv import AppVerificationService

manualParametersDict = dict(
    default=[manualParametersDictCons.get("default")],
)

operation_id = dict(
    login_with_otp="لاگین > دریافت کد ورود",
    login_validate_otp="لاگین > اعتبارسنجی کد ورود",
    user_information_get="لاگین > نمایش اطلاعات کاربر",
    user_information_post="لاگین > ارسال اطلاعات کاربر",
)

tags = ['verification/احراز هویت']
operationDescriptionsDict = dict()
get_swagger_kwargs = SwaggerAutoSchemaKwargs(
    manualParametersDict, operationDescriptionsDict, tags, operation_id
).get_kwargs


class AppVerificationAPI(viewsets.ViewSet):
    permission_classes = [AllowAny]

    serializers_dict = dict(
        POST=dict(
            login_with_otp={
                "request_body": AppLoginCreateOtpSerializer,
                "responses": {200: "OK"},
            },
            login_validate_otp={
                "request_body": AppLoginValidateOtpSerializer,
                "responses": {200: AppLoginCreateTokenSerializer},
            },
            user_information_post={
                "request_body": AppUserInformationPostSerializer,
                "responses": {200: "OK"},
            }
            ),
        GET=dict(
            user_information_get={
                "responses": {200: AppUserInformationGetSerializer},
            }
        ),
    )

    def get_serializer_class(self):
        return (
            self.serializers_dict.get(self.request.method)
            .get(self.action)
            .get("request_body")
        )

    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="POST",
            action_name="login_with_otp",
            serializer=serializers_dict.get("POST"),
        )
    )
    @action(methods=["POST"], detail=False, url_path="login/create_otp")
    def login_with_otp(self, request, **kwargs):
        """
        send otp code to users phone number
        """
        serializer = AppLoginCreateOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validate_data = serializer.validated_data

        code = AppVerificationService.create_redis_otp_code(validate_data.get('phone_number'),
                                                            otp_code_length=validate_data.get('otp_code_length'),
                                                            expire_time=validate_data.get('expire_time'))
        sms_data = [{
            'company_name': "شبکه اجتماعی",
            "otp_code": str(code),
            'signature': validate_data.get('signature', None),
            'phone_number': validate_data.get('phone_number'),
            'sms_type': 'login_create_otp',
        }]

        SmsCreatorService()(sms_data=sms_data)
        return Response("OK")

    @swagger_auto_schema(
        **get_swagger_kwargs(
            method="POST",
            action_name="login_validate_otp",
            serializer=serializers_dict.get("POST"),
        )
    )
    @action(methods=["POST"], detail=False, url_path="login/validate_otp")
    def login_validate_otp(self, request, **kwargs):
        """
        validate otp code and get or create user
        output: jwt token
        """
        serializer = AppLoginValidateOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AppVerificationService.validate_redis_otp_code(**serializer.validated_data)
        user = User.objects.filter(phone_number=serializer.validated_data.get('phone_number')).first()
        if user and has_role(user, UserRoleChoice.CUSTOMER):
            pass
        else:
            user = User.objects.create(username=f'customer_{serializer.validated_data.get("phone_number")}',
                                       phone_number=serializer.validated_data.get("phone_number"))
            user.set_password(str(uuid.uuid4))
            assign_role(user=user, role=UserRoleChoice.CUSTOMER)
            CustomerProfile.objects.get_or_create(user=user)

        refresh = AppLoginValidateOtpSerializer.get_token(user)
        data = {"refresh": str(refresh), "access": str(refresh.access_token)}
        AppVerificationService.delete_redis_otp_code(phone_number=user.phone_number)
        return Response(data)

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
    @action(methods=["GET", "POST"], detail=False, parser_classes=(FormParser, MultiPartParser), permission_classes=[IsAuthenticated])
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
