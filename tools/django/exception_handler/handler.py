from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.signals import got_request_exception
from django.db.models import ProtectedError
from django.http import Http404
from django.utils.translation import activate
from django.utils.translation import gettext as _
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.settings import api_settings as drf_api_settings
from rest_framework.views import set_rollback

from .exceptions import ProtectedObjectException
from .settings import api_settings
from .utils import ensure_string

DEFAULT_ERROR_DETAIL = _("A server error occurred.")


class ErrorTypes(Enum):
    """
    Defines default error types. Custom error types are still supported by
    setting the `exception_type` or `default_type` attributes on an instance exception.
    """

    authentication_error = "authentication_error"
    invalid_request = "invalid_request"
    server_error = "server_error"
    throttled_error = "throttled_error"
    validation_error = "validation_error"
    multiple_exceptions = "multiple"
    single_exceptions = "single"


@ensure_string
def _get_error_type(exc) -> Union[str, ErrorTypes]:
    """
    Gets the `type` for the exception. Default types are defined for base DRF exceptions.
    """
    if hasattr(exc, "exception_type"):
        # Attempt first to get the type defined for this specific instance
        return exc.exception_type
    elif hasattr(exc, "default_type"):
        # Use the exception class default type if available
        return exc.default_type

    # Default configuration for DRF exceptions
    if isinstance(exc, exceptions.AuthenticationFailed):
        return ErrorTypes.authentication_error
    elif isinstance(exc, exceptions.MethodNotAllowed):
        return ErrorTypes.invalid_request
    elif isinstance(exc, exceptions.NotAcceptable):
        return ErrorTypes.invalid_request
    elif isinstance(exc, exceptions.NotAuthenticated):
        return ErrorTypes.authentication_error
    elif isinstance(exc, exceptions.NotFound):
        return ErrorTypes.invalid_request
    elif isinstance(exc, exceptions.ParseError):
        return ErrorTypes.invalid_request
    elif isinstance(exc, exceptions.PermissionDenied):
        return ErrorTypes.authentication_error
    elif isinstance(exc, exceptions.Throttled):
        return ErrorTypes.throttled_error
    elif isinstance(exc, exceptions.UnsupportedMediaType):
        return ErrorTypes.invalid_request
    elif isinstance(exc, exceptions.ValidationError):
        return ErrorTypes.validation_error

    # Couldn't determine type, default to generic error
    return ErrorTypes.server_error


def _normalize_exception_codes(
    exception_codes: Dict,
    parent_key: List[str] = None,
) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Returns a normalized one-level dictionary of exception attributes and codes. Used to
    standardize multiple exceptions and complex nested exceptions.
    Example:
     => [
         {
             "parsed_keys": ["form", "password"],
             "exception_code": ["required"]
         },
         {
             "parsed_keys": ["form", "password"],
             "exception_code": "min_length"
         }
     ]
    """
    if parent_key is None:
        parent_key = []

    items: List = []
    for key, exception_code in exception_codes.items():

        keys: List[str] = parent_key + [key]

        if isinstance(exception_code, dict):
            items.extend(
                _normalize_exception_codes(
                    exception_code.copy(),
                    keys,
                )
            )
        else:
            items.append({"parsed_keys": keys, "exception_code": exception_code})
    return items


def _get_main_exception_and_code(
    exception_codes: Union[Dict, str, List]
) -> Tuple[str, Optional[str]]:
    def override_or_return(code: str) -> str:
        """
        Returns overridden code if needs to change or provided code.
        """
        if code == "invalid":
            # Special handling for validation errors. Use `invalid_input` instead
            # of `invalid` to provide more clarity.
            return "invalid_input"

        return code

    # Get base exception codes from DRF (if exception is DRF)
    if exception_codes:
        codes = exception_codes

        if isinstance(codes, dict) and "parsed_keys" in codes:
            # Handling for parsed nested attributes (see `_normalize_exception_codes`)
            code = (
                codes["exception_code"][0]
                if isinstance(codes["exception_code"], list)
                else codes["exception_code"]
            )
            return override_or_return(str(code)), codes["parsed_keys"]

        if isinstance(codes, str):
            # Only one exception, return
            return codes, None
        elif isinstance(codes, dict):
            # If object is a dict or nested dict, return the key of the very first error
            key = next(iter(codes))  # Get initial key
            code = codes[key] if isinstance(codes[key], str) else codes[key][0]
            return override_or_return(code), key
        elif isinstance(codes, list):
            return override_or_return(str(codes[0])), None

    return "error", None


@ensure_string
def _get_detail(exc, exception_key: Union[str, List[str]] = "") -> str:
    """
    Returns the human-friendly detail text for a specific insight exception.
    """

    if hasattr(exc, "detail"):
        # Get exception details if explicitly set. We don't obtain exception information
        # from base Python exceptions to avoid leaking sensitive information.
        if isinstance(exc.detail, str):
            return str(
                exc.detail
            )  # We do str() to get the actual error string on ErrorDetail instances
        elif isinstance(exc.detail, dict):
            value = exc.detail

            # Handle nested attributes
            if isinstance(exception_key, list):
                for key in exception_key:
                    value = value[key]
            if isinstance(value, dict):
                return value.get("detail", "")
            return str(value if isinstance(value, str) else value[0])
        elif isinstance(exc.detail, list) and len(exc.detail) > 0:
            return exc.detail[0]

    return DEFAULT_ERROR_DETAIL


def _get_farsi_detail(exception_code, detail, attr):
    if exception_code and detail:
        activate("fa")
        return _(detail)
    return None


def _get_attr(exception_key: Optional[Union[str, List[str]]] = None) -> Optional[str]:
    """
    Returns the offending attribute name. Handles special case
        of __all__ (used for instance in UniqueTogetherValidator) to return `None`.
    """

    def override_or_return(final_key: Optional[str]) -> Optional[str]:
        """
        Returns overridden code if needs to change or provided code.
        """
        if final_key == "__all__":
            return None

        if final_key == drf_api_settings.NON_FIELD_ERRORS_KEY:
            return None

        return final_key if final_key else None

    if isinstance(exception_key, list):
        cp_exception_key = []
        for item in exception_key:
            if type(item) == int:
                item = str(item)
            cp_exception_key.append(item)

        return override_or_return(api_settings.NESTED_KEY_SEPARATOR.join(cp_exception_key))

    return override_or_return(exception_key)


def _get_http_status(exc) -> int:
    if exc.default_code in ["authentication_failed", "not_authenticated"]:
        return status.HTTP_401_UNAUTHORIZED
    return exc.status_code if hasattr(exc, "status_code") else status.HTTP_500_INTERNAL_SERVER_ERROR


def exception_reporter(exc: BaseException, context: Optional[Dict] = None) -> None:
    """
    Logic for reporting an exception to any APMs.
    Example:
        if not isinstance(exc, exceptions.APIException):
            capture_exception(exc)
    """
    pass


def exception_handler(exc: BaseException, context: Optional[Dict] = None) -> Optional[Response]:
    # Special handling for Django base exceptions first
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()
    elif isinstance(exc, ProtectedError):
        exc = ProtectedObjectException(
            "",
            protected_objects=exc.protected_objects,
        )
    elif isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if (
        # getattr(settings, "DEBUG", False)
        not api_settings.ENABLE_IN_DEBUG
        and not isinstance(exc, exceptions.APIException)
    ):
        # By default don't handle non-DRF errors in DEBUG mode, i.e. Django will treat
        # unhandled exceptions regularly (very evident yellow error page)

        # NOTE: to make sure we get exception tracebacks in test responses, we need
        # to make sure this signal is called. The django test client uses this to
        # pull out the exception traceback.
        #
        # See https://github.com/django/django/blob/3.2.9/django/test/client.py#L712
        got_request_exception.send(
            sender=None,
            request=context["request"] if context and "request" in context else None,
        )
        return None

    if isinstance(exc, exceptions.ValidationError):
        codes = exc.get_codes()
        if type(codes) is list:
            exception_list = [codes]
        else:
            exception_list = _normalize_exception_codes(codes)
    elif hasattr(exc, "get_codes"):
        exception_list = [exc.get_codes()]  # type: ignore
    else:
        exception_list = [None]

    exception_list = [_get_main_exception_and_code(exception) for exception in exception_list]

    api_settings.EXCEPTION_REPORTING(exc, context)

    set_rollback()
    exception_code, exception_key = exception_list[0]
    attr = _get_attr(exception_key)
    if _get_attr(exception_key) is None:
        if "must make a unique set" in _get_detail(exc, exception_key):
            attr = _get_detail(exc, exception_key).split(" ")[2][:-1]
        # elif context.get('view').action:
        #     attr = context.get('view').action
    activate("fa")
    if api_settings.FARSI_EXCEPTION:
        response = dict(
            type=_get_error_type(exc),
            code=exception_code,
            detail=_get_detail(exc, exception_key),
            attr=attr,
            fa_attr=_(attr) if attr else None,
            fa_details=_get_farsi_detail(exception_code, _get_detail(exc, exception_key), attr),
        )
    else:
        response = dict(
            type=_get_error_type(exc),
            code=exception_code,
            detail=_get_detail(exc, exception_key),
            attr=attr,
        )

    return Response(response, status=_get_http_status(exc))
