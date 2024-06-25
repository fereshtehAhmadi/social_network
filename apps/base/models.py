import datetime

from django.db import models
from rest_framework.exceptions import ValidationError
from rest_framework.validators import qs_exists

from tools.django.dynamic_attr import get_dynamic_attr
from tools.project.common.error_messages import ErrorMessagesCons


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    STR_RETURN_LIST = ["pk"]
    UNIQUE_CHECK_LIST = []

    class Meta:
        abstract = True
        ordering = ("id",)

    def __str__(self):
        map_list = [str(get_dynamic_attr(self, field)) for field in self.STR_RETURN_LIST]
        return "    ".join(map_list)

    @property
    def creation_datetime_ts(self):
        return self.creation_datetime.timestamp()

    @property
    def update_datetime_ts(self):
        return self.update_datetime.timestamp()

    @property
    def convert_to_date_format(self, date):
        return datetime.datetime.strptime(str(date), "%Y-%m-%d").timestamp()

    def run_unique_validation(self):
        """check unique or unique together validation"""
        for field_pack, condition in self.UNIQUE_CHECK_LIST:
            if isinstance(field_pack, str):
                field_pack = [field_pack]
            elif not isinstance(field_pack, tuple) and not isinstance(field_pack, list):
                raise ValueError("field_pack value in models should be string, tuple or list")

            fields = {f"{field}": getattr(self, field) for field in field_pack}
            queryset = self.__class__.available_objects.filter(condition, **fields)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)

            if qs_exists(queryset):
                raise ValidationError(
                    detail={f"{field_pack[0]}": ErrorMessagesCons.unique},
                    code=ErrorMessagesCons.unique.name,
                )
