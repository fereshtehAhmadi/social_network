from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.application.verification.serializers import AppLoginCreateOtpSerializer
from tools.project.common.constants.cons import manualParametersDictCons
from tools.project.sms.service import SmsCreatorService
from tools.project.swagger_tools import SwaggerAutoSchemaKwargs
from tools.project.verification_serv import AppVerificationService

manualParametersDict = dict(
    default=[manualParametersDictCons.get("default")],
)

operation_id = dict(
    login_with_otp="لاگین > دریافت کد ورود",
    login_validate_otp="لاگین > اعتبارسنجی کد ورود",
)

tags = []
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
            # login_validate_otp={
            #     "request_body": CustomerAppLoginValidateOtpInputSerializer,
            #     "responses": {200: CustomerAppLoginValidateOtpOutputSerializer},
            # },
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
        serializer = AppLoginCreateOtpSerializer(request.data)
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

    # @swagger_auto_schema(
    #     **get_swagger_kwargs(
    #         method="POST",
    #         action_name="login_validate_otp",
    #         serializer=serializers_dict.get("POST"),
    #     )
    # )
    # @action(methods=["POST"], detail=False, url_path="login/validate_otp")
    # def login_validate_otp(self, request, **kwargs):
    #     """
    #     :post: Validate otp code sent for entered phone_number \n
    #
    #     :param request: post request object
    #     :param kwargs: None
    #
    #     :return:
    #         - post: refresh and access token json, 200 status code
    #     :rtype:
    #         - post: json
    #
    #     """
    #     pass

