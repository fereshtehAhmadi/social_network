from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from tools.project.common.validators import PhoneNumberValidator


class AppLoginCreateOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=11,
        min_length=11,
        required=True,
        allow_null=False,
        allow_blank=False,
        validators=[PhoneNumberValidator],
    )
    otp_code_length = serializers.IntegerField(default=5, allow_null=False, min_value=3)
    expire_time = serializers.IntegerField(
        default=120,
        allow_null=False,
        min_value=60,
        help_text="please enter expire time in second",
    )
    signature = serializers.CharField(
        max_length=20,
        required=False,
        allow_null=False,
        allow_blank=False,
    )


class AppLoginValidateOtpSerializer(serializers.Serializer):
    code = serializers.CharField(allow_null=False, allow_blank=False)
    phone_number = serializers.CharField(max_length=11, min_length=11, required=True, allow_null=False,
                                         allow_blank=False,
                                         validators=[PhoneNumberValidator])
    token_class = RefreshToken

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class AppLoginCreateTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
