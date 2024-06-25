from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import ValidationError

from tools.project.common.error_messages import ErrorMessagesCons


class PhoneNumberValidator(RegexValidator):
    regex = r"^0\d{10}$"
    message = _("Phone number is not valid.")


def username_existence_validator(queryset, **filter_kwargs):
    filter_result = queryset.get_or_none(**filter_kwargs)
    if not filter_result:
        raise ValidationError(
            detail={"message": ErrorMessagesCons.no_user_with_username},
            code=ErrorMessagesCons.no_user_with_username.name,
        )
    return filter_result
