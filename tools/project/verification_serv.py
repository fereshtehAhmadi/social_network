import random
import string

import redis
from django.conf import settings
from rest_framework.exceptions import ValidationError


class AppVerificationService:

    @staticmethod
    def check_otp_code_expiration(phone_number):
        """ check if otp code is expired or not
        user can not create new otp before expiration time
        """
        r = redis.StrictRedis()
        if r.exists(phone_number):
            raise ValidationError(detail={'message': 'Try after 2 minutes'},
                                  code='otp_code_expire_time')

    @classmethod
    def create_redis_otp_code(cls, phone_number, otp_code_length, expire_time, **kwargs):
        """create a random code base on otp_code_length and expire_time using redis"""
        # self.check_otp_code_expiration(phone_number)
        r = redis.StrictRedis()
        if getattr(settings, 'DEBUG') is True:
            code = '5' * otp_code_length
        else:
            code = ''.join(random.choices(string.digits[1:], k=otp_code_length))
        r.set(phone_number, code)
        r.expire(phone_number, expire_time)
        return code

    @staticmethod
    def validate_redis_otp_code(phone_number, code, **kwargs):
        """check otp code is not expired and is not wrong"""
        r = redis.StrictRedis()
        if not r.exists(phone_number):
            raise ValidationError(detail={'message': 'Otp code is expired'}, code='otp_code_expired')

        if code != r.get(phone_number).decode("utf-8"):
            raise ValidationError(detail={'message': 'Incorrect otp code'}, code='wrong_otp_code')
