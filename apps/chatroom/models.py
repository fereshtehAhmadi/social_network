import random

from django.db import models
from django.db.models import Q

from apps.base.models import BaseModel


class Connection(BaseModel):
    customer = models.ForeignKey('profiles.CustomerProfile', on_delete=models.PROTECT, related_name='connections')
    connection = models.ForeignKey('profiles.CustomerProfile', on_delete=models.PROTECT, related_name='my_connections')

    STR_RETURN_LIST = ["pk"]

    class Meta:
        verbose_name = "Connection"
        verbose_name_plural = "Connection"
        default_related_name = "connections"


class ChatRoom(BaseModel):
    customer_profile = models.ForeignKey('profiles.CustomerProfile', on_delete=models.CASCADE)
    new_messages = models.IntegerField(default=0)

    STR_RETURN_LIST = ["pk", "customer_profile__user__id"]
    UNIQUE_CHECK_LIST = [(["customer_profile"], Q())]

    class Meta:
        verbose_name = "Chat Room"
        verbose_name_plural = "Chat Room"
        default_related_name = "chat_rooms"


class Message(BaseModel):
    def file_message_path(self, filename):
        return "messages/{0}/file_message/{1}".format(
            str(self.id),
            "_".join([filename, str(random.randint(1000000000, 9999999999))]),
        )

    sender = models.ForeignKey('profiles.CustomerProfile', on_delete=models.PROTECT, related_name='sender_messages')
    receiver = models.ForeignKey('profiles.CustomerProfile', on_delete=models.PROTECT, related_name='receiver_messages')
    message = models.TextField(null=True, blank=True)
    file_message = models.FileField(
        max_length=500,
        null=True, blank=True,
        upload_to=file_message_path,
    )
    seen = models.BooleanField(default=True)

    STR_RETURN_LIST = ["pk", "sender__user__id"]

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Message"
        default_related_name = "messages"
