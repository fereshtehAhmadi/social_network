from django.db import transaction
from rest_framework.utils import model_meta


class BaseModelServiceClass:

    @staticmethod
    def get_model_fields(model, fields: list = None, exclude_fields: list = None, **kwargs) -> dict:

        # Get all the fields from the model
        model_fields = {field.name for field in model._meta.get_fields()}

        if fields is None or fields == '__all__':
            fields = []

        if exclude_fields is None:
            exclude_fields = []
        elif exclude_fields == '__all__':
            exclude_fields = model_fields

        if fields:
            model_fields.intersection_update(fields)
        if exclude_fields:
            model_fields.difference_update(exclude_fields)

        # Filter the kwargs based on the final set of field names
        filtered_fields = {key: value for key, value in kwargs.items() if key in model_fields}

        return filtered_fields

    def create_validate(self, **kwargs):
        return kwargs

    def update_validate(self, instance, **kwargs):
        return instance, kwargs

    @transaction.atomic
    def create(self, **kwargs):
        kwargs = self.create_validate(**kwargs)
        ModelClass = self.Meta.model
        fields = self.get_model_fields(model=ModelClass,
                                       fields=getattr(self.Meta, "create_fields", None),
                                       exclude_fields=getattr(self.Meta, "create_exclude_fields", None),
                                       **kwargs)

        # Remove many-to-many relationships from fields.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in fields):
                many_to_many[field_name] = fields.pop(field_name)

        instance = ModelClass(**fields)
        instance.full_clean()
        instance.save()

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance

    @transaction.atomic
    def update(self, instance, **kwargs):
        instance, kwargs = self.update_validate(instance, **kwargs)
        ModelClass = self.Meta.model
        fields = self.get_model_fields(model=ModelClass,
                                       fields=getattr(self.Meta, "update_fields", None),
                                       exclude_fields=getattr(self.Meta, "update_exclude_fields", None),
                                       **kwargs)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        m2m_fields = []
        for attr, value in fields.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.full_clean()
        instance.save()

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance

    @transaction.atomic
    def delete(self, instance):
        instance.delete()

    @transaction.atomic
    def restore(self, instance):
        instance.restore()
        return instance

    class Meta:
        model = None
        create_fields = []
        update_fields = []
