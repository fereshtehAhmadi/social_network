from django.db import models

from apps.base.models import BaseModel


class Connection(BaseModel):
    customer = models.ForeignKey('profiles.CustomerProfile', on_delete=models.PROTECT, related_name='connections')
    connection = models.ForeignKey('profiles.CustomerProfile', on_delete=models.PROTECT, related_name='my_connections')
    accepted = models.BooleanField(null=True, blank=True)

    STR_RETURN_LIST = ["pk"]

    class Meta:
        verbose_name = "Connection"
        verbose_name_plural = "Connection"
        default_related_name = "connections"
