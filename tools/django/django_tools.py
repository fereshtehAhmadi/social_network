import datetime
import functools
import re

from rest_framework.exceptions import ValidationError

from tools.project.validators.general_validators import QueryParameterValidator, TryExceptDjangoCoreValidators


def get_dynamic_attr(obj, name, default=None):
    related_names = name.split('.')
    if not obj:
        return default
    for related_name in related_names:
        obj = getattr(obj, related_name)
        if hasattr(obj, 'get_queryset'):
            obj = obj.first()
        if isinstance(obj, bool):
            return obj
        if not obj:
            return default
    return obj


def get_dynamic_dict_value(dictionary, name, default=None):
    related_names = name.split('.')

    for related_name in related_names:
        if related_name == 'True':
            related_name = True
        elif related_name == 'False':
            related_name = False
        dictionary = dictionary.get(related_name, None)
        if not dictionary:
            return default
        if not isinstance(dictionary, dict):
            return dictionary

    return dictionary


def check_api_params(params_list: list, required: bool = True, allow_null: bool = False,
                     allow_blank: bool = False, methods: list = ['POST', 'GET', 'DELETE', 'PATCH', 'PUT']):
    """
    check if required parameters exists in request.GET keys based on kwargs conditions like required, allow_null and
    allow_blank
    raise ValidationError if there was a problem with required parameters
    """

    def decorated_api(func):

        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            request = args[1]
            if request.method in methods:
                if isinstance(params_list, str):
                    params = list(params_list)
                elif isinstance(params_list, list):
                    params = params_list
                else:
                    raise ValidationError(detail={'params_list': 'This value should be a list.'},
                                          code='value_type')

                TryExceptDjangoCoreValidators(validator=QueryParameterValidator(limit_value=params,
                                                                                required=required,
                                                                                allow_null=allow_null,
                                                                                allow_blank=allow_blank))(request.GET)
            return func(*args, **kwargs)

        return wrapper_func

    return decorated_api
