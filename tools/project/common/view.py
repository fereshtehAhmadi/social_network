from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import GenericViewSet

from tools.project.common.error_messages import ErrorMessagesCons
from rest_framework.generics import get_object_or_404


class CommonGenericViewSet(GenericViewSet):
    InputSerializer = None
    OutputSerializer = None
    ListOutputSerializer = None

    def validate_with_input_serializer(
            self, data: dict = None, input_serializer=None, instance=None, **kwargs
    ) -> dict:
        """
        Validate the request data with given serializer or input serializer of view and return validated data
        """
        data = data or self.request.data
        input_serializer = input_serializer or self.InputSerializer
        if instance:
            ser = input_serializer(data=data, instance=instance, partial=kwargs.get("partial"))
        else:
            ser = input_serializer(data=data, partial=kwargs.get("partial"))
        ser.is_valid(raise_exception=True)
        return ser.validated_data

    def get_object(self, *args, **kwargs):
        try:
            if kwargs.get("queryset"):
                lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
                assert lookup_url_kwarg in self.kwargs, (
                        'Expected view %s to be called with a URL keyword argument '
                        'named "%s". Fix your URL conf, or set the `.lookup_field` '
                        'attribute on the view correctly.' %
                        (self.__class__.__name__, lookup_url_kwarg)
                )
                filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
                obj = get_object_or_404(kwargs.get("queryset"), **filter_kwargs)

                # May raise a permission denied
                self.check_object_permissions(self.request, obj)
                return obj
            else:
                return super().get_object()
        except Http404:
            raise ValidationError(
                {f"{str(self.get_queryset().model.__name__).lower()}": ErrorMessagesCons.does_not_exist},
                code=ErrorMessagesCons.does_not_exist.name,
            )
