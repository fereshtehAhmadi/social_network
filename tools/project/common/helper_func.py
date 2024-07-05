from django.core import exceptions


class FactoryGetObject:
    """
    a class is factory pattern for
    get a object
    """

    @classmethod
    def find_object(cls, object_type, *args, **kwargs):
        try:
            if hasattr(object_type, "is_active") and "is_active" not in kwargs:
                kwargs.update({"is_active": True})
            return object_type.objects.get(*args, **kwargs)
        except:
            name = str(object_type).split(".")[-1][0:-2]
            raise exceptions.ValidationError(
                message={name: "Object Not Found"}, code="does_not_exist"
            )

    @classmethod
    def filter_object(cls, object_type, *args, **kwargs):
        if hasattr(object_type, "is_active"):
            kwargs.update({"is_active": True})
        return object_type.objects.filter(*args, **kwargs)

    @classmethod
    def find_object_active_independent(cls, object_type, *args, **kwargs):
        try:
            return object_type.objects.get(*args, **kwargs)
        except:
            name = str(object_type).split(".")[-1][0:-2]
            raise exceptions.NotFound(detail=f"{name} was not found")
