from django.db import models

from apps.base.models import BaseModel


class Connection(BaseModel):
    sender = models.ForeignKey('profiles.CustomerProfile', on_delete=models.PROTECT, related_name='connection_sender')
    receiver = models.ForeignKey('profiles.CustomerProfile', on_delete=models.PROTECT, related_name='connection_receiver')
    accepted = models.BooleanField(null=True, blank=True)

    STR_RETURN_LIST = ["pk"]

    class Meta:
        verbose_name = "Connection"
        verbose_name_plural = "Connection"
        default_related_name = "connections"
