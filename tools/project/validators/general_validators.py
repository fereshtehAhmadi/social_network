from django.core.validators import BaseValidator
from django.http import QueryDict
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError, _get_error_details
from django.core.exceptions import ValidationError as DjangoValidationError


@deconstructible
class QueryParameterValidator(BaseValidator):
    code = "invalid_query_parameter"
    message = _("Query parameter is not valid.")

    def __init__(
            self,
            limit_value: list,
            required: bool = True,
            allow_null: bool = False,
            allow_blank: bool = False,
    ):
        """
        :param limit_value: list of parameters name which needs validation
        :param required: check if parameter is sent
        :param allow_null: check parameter nullable
        :param allow_blank: check parameter blank string
        """
        if isinstance(limit_value, str):
            self.limit_value = [limit_value]
        elif isinstance(limit_value, tuple):
            self.limit_value = list(limit_value)
        else:
            self.limit_value = limit_value
        self.required = required
        self.allow_null = allow_null
        self.allow_blank = allow_blank

    def __call__(self, value: QueryDict):
        """
        :param value: request.GET
        :return:
        """
        cleaned = self.clean(value)
        limit_value = (
            self.limit_value() if callable(self.limit_value) else self.limit_value
        )
        for parameter in limit_value:
            params = {"limit_value": parameter, "show_value": cleaned, "value": value}
            if self.compare(cleaned, parameter):
                raise DjangoValidationError(self.message, code=self.code, params=params)

    def compare(self, value: dict, parameter):
        if self.required:
            if parameter not in value.keys():
                self.message = _(f"{parameter} Query parameter is required.")
                return True
        if not self.allow_null:
            if (
                    value.get(parameter, None) is None
                    or value.get(parameter, None) == "null"
            ):
                self.message = _(f"{parameter} Query parameter may not be null.")
                return True
        if not self.allow_blank:
            if value.get(parameter, "") == "":
                self.message = _(f"{parameter} Query parameter may not be blank.")
                return True
        return False

    def clean(self, value: QueryDict):
        """
        :param value: request.GET
        :return: convert request.GET OrderedDict to dict
        """
        value = value.dict()
        return value


@deconstructible
class QueryParameterValueOptionsValidator(BaseValidator):
    code = "invalid_query_parameter"
    message = _("Query parameter value '%(value)s' is not valid.")

    def __init__(self, limit_value: list):
        """
        :param limit_value: valid options of given query parameter
        """
        if isinstance(limit_value, str):
            self.limit_value = [limit_value]
        elif isinstance(limit_value, tuple):
            self.limit_value = list(limit_value)
        else:
            self.limit_value = limit_value

    def __call__(self, param_value):
        """
        :param param_value: request.GET
        :return:
        """
        cleaned = self.clean(param_value)
        limit_value = (
            self.limit_value() if callable(self.limit_value) else self.limit_value
        )
        params = {
            "limit_value": f"{limit_value}",
            "show_value": cleaned,
            "value": param_value,
        }
        if self.compare(cleaned, limit_value):
            raise DjangoValidationError(self.message, code=self.code, params=params)

    def compare(self, param_value, options):
        if param_value not in options:
            return True
        return False


class RestValidationError(ValidationError):
    default_detail = _("Invalid input.")
    default_code = "invalid"

    def __init__(self, detail=None, code=None, params=None, field=None):
        if detail is None:
            detail = self.default_detail
        else:
            detail = str(detail) % params
        if code is None:
            code = self.default_code
        if field is not None and isinstance(field, str):
            detail = {field: detail}
        elif params and params.get("limit_value", None):
            detail = {params.get("limit_value"): detail}
        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)


class TryExceptDjangoCoreValidators:
    def __init__(self, validator, field=None):
        """
        :param validator: class of BaseValidators
        :param field: name of validation field
        usage example : TryExceptDjangoCoreValidators(validator=ValueStartsWithValidator(limit_value='0'),
        field='insurance')('8')
        """
        self.validator = validator
        self.field = field

    def __call__(self, *args, **kwargs):
        try:
            self.validator.__call__(*args, **kwargs)
        except DjangoValidationError as exc:
            raise RestValidationError(
                detail=exc.message, code=exc.code, params=exc.params, field=self.field
            )
        except ValidationError as exc:
            raise ValidationError(exc)