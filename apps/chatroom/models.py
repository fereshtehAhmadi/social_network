import random

from decouple import config
from django.db import models
from django.db.models import Q

from apps.base.models import BaseModel


class NewMessage(BaseModel):
    customer = models.ForeignKey('profiles.CustomerProfile', on_delete=models.CASCADE)
    new_messages = models.IntegerField(default=0)

    STR_RETURN_LIST = ["pk", "customer_profile__user__id"]
    UNIQUE_CHECK_LIST = [(["customer_profile"], Q())]

    class Meta:
        verbose_name = "New Message"
        verbose_name_plural = "New Message"
        default_related_name = "new_messages"


class ChatRoom(BaseModel):
    sender = models.ForeignKey('profiles.CustomerProfile', on_delete=models.CASCADE)
    receiver = models.ForeignKey('profiles.CustomerProfile', on_delete=models.CASCADE,
                                 related_name='chatroom_receiver')
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
            str(self.pk),
            "_".join([filename, str(random.randint(1000000000, 9999999999))]),
        )

    sender = models.ForeignKey('profiles.CustomerProfile', on_delete=models.PROTECT, related_name='sender_messages')
    receiver = models.ForeignKey('profiles.CustomerProfile', on_delete=models.PROTECT, related_name='receiver_messages')
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)
    message = models.TextField(null=True, blank=True)
    file_message = models.FileField(
        max_length=500,
        null=True, blank=True,
        upload_to=file_message_path,
    )
    seen = models.BooleanField(default=True)
    url_serve = models.CharField(max_length=1000, null=True, blank=True)

    STR_RETURN_LIST = ["pk", "sender__user__id"]

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Message"
        default_related_name = "messages"

    def get_dynamic_url(self):
        if self.file_message:
            if self.url_serve is None:
                self.save()
                image_url_serve = config("IMAGE_URL_SERVE")
                return image_url_serve + "/media/" + self.file_message.name
            return self.url_serve + "/media/" + self.file_message.name
        else:
            return None
