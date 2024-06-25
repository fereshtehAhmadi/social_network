from drf_yasg import openapi


class SwaggerAutoSchemaKwargs:
    def __init__(self, manual_parameter_dict: dict = None, operation_description_dict: dict = None, tags: list = None,
                 operation_id_dict: dict = None):
        self.manualParametersDict = manual_parameter_dict
        self.operationDescriptionsDict = operation_description_dict
        self.tags = tags
        self.operation_id_dict = operation_id_dict

    def get_operation_id(self, action_name):
        if isinstance(self.operation_id_dict, str):
            return self.operation_id_dict
        elif isinstance(self.operation_id_dict, dict):
            return self.operation_id_dict.get(action_name, action_name)
        else:
            return action_name

    def get_kwargs(self, method, action_name, serializer, **kwargs) -> dict:
        """
        :param method: GET, POST, PATCH, DELETE
        :param serializer: swagger serializers
        :param action_name: request action name
        :return: dict of swagger auto schema attributes
        """
        operation_id = self.get_operation_id(action_name=action_name)
        response = {"method": method, 'manual_parameters': [],
                    'operation_id': operation_id}

        if self.manualParametersDict.get(action_name, None):
            response['manual_parameters'].extend(self.manualParametersDict.get(action_name))

        if self.manualParametersDict.get('default', None):
            response['manual_parameters'].extend(self.manualParametersDict.get('default'))

        if self.operationDescriptionsDict.get(action_name, None):
            response.update(
                {
                    "operation_description": self.operationDescriptionsDict.get(
                        action_name
                    )
                }
            )
        if self.tags is not None:
            response.update({"tags": self.tags})

        response.update(serializer.get(action_name))
        return response


rest_framework_openapi_field_mapping = {
    "ListField": openapi.TYPE_ARRAY,
    "CharField": openapi.TYPE_STRING,
    "BooleanField": openapi.TYPE_BOOLEAN,
    "FloatField": openapi.TYPE_NUMBER,
    "DateTimeField": openapi.TYPE_STRING,
    "IntegerField": openapi.TYPE_INTEGER,
    "SerializerMethodField": openapi.TYPE_STRING,
    "FileField": openapi.TYPE_FILE,
    "URLField": openapi.FORMAT_URI,
}


def parse_rest_framework_field(field):
    rest_framework_field_type = field.split("(")[0]
    openapi_field_type = rest_framework_openapi_field_mapping[rest_framework_field_type]
    if "help_text=" in field:
        field_description = field.split("help_text='")[-1].split("'")[0]
    else:
        field_description = None
    return openapi.Schema(type=openapi_field_type, description=field_description)


def parse_serializer(serializer):
    properties = {}
    if getattr(serializer, 'many', False):
        serializer = serializer.child
    for k, v in serializer.get_fields().items():
        if v.__module__ == "rest_framework.fields":
            properties[k] = parse_rest_framework_field(str(v))
        elif v.__module__.startswith("apps."):
            serializer = str(v).strip().split("(")[0]
            exec(f"from {v.__module__} import {serializer}")
            eval_serializer = eval(f"{serializer}()")
            properties[k] = openapi.Schema(type=openapi.TYPE_OBJECT, properties=parse_serializer(eval_serializer))
        else:
            pass
    return properties


def serializer_to_schema(serializer, description=None):
    """ Needs to return openapi.Schema() """
    properties = parse_serializer(serializer)
    return_openapi_schema = openapi.Schema(type=openapi.TYPE_OBJECT, properties=properties, description=description)
    return return_openapi_schema
