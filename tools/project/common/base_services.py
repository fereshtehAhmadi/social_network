from tools.project.common.helper_func import FactoryGetObject


class FactoryServiceClass:
    """Factory class for agent and customer views"""

    services_dicts = {}

    def __init__(self, **kwargs):
        """
        get api action name and find service class based
        """

        self.action_name = kwargs.get("action_name", None) or kwargs.get("view_cls").action
        service_dict = self.services_dicts.get(self.action_name)
        self.service_instance = service_dict.get("default")(**kwargs)

    def __call__(self, *args, **kwargs):
        """
        call method of service instance based in action name
        """
        return getattr(self.service_instance, self.action_name)(kwargs.get("output_serializer"))


class BaseServiceClass:
    def __init__(self, request, input_serializer=None, **kwargs):
        self.request = request
        self.initial_data = request.data
        self.input_serializer = input_serializer
        self.kwargs = kwargs

    def validate_data(self, initial_data, context=None, many=False):
        """
        validate initial data and return validated data
        """

        if context:
            data = self.input_serializer(data=initial_data, context=context, many=many)
        else:
            data = self.input_serializer(data=initial_data, many=many)
        data.is_valid(raise_exception=True)
        return data.validated_data

    def save_validated_data(self, initial_data, context=None, many=False):
        if context:
            data = self.input_serializer(data=initial_data, context=context, many=many)
        else:
            data = self.input_serializer(data=initial_data, many=many)
        data.is_valid(raise_exception=True)
        instance = data.save()
        return instance

    @staticmethod
    def return_response(instance=None, output_serializer=None, many=False):
        if output_serializer:
            return output_serializer(instance=instance, many=many).data
        return "OK"

    def get_object_by_pk(self, instance_model, path_param_name="pk", **filters):
        return FactoryGetObject.find_object(
            instance_model, pk=self.kwargs.get("view_cls").kwargs.get(path_param_name), **filters
        )

    @staticmethod
    def find_model_valid_fields(model_cls, data):
        response = dict(filter(lambda item: hasattr(model_cls, item[0]), dict(data).items()))
        return response
