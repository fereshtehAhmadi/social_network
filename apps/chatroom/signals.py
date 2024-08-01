import datetime

from decouple import config
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.chatroom.models import Message


@receiver(pre_save, sender=Message)
def pre_save_images(sender, instance, **kwargs):
    file_field_updated = False
    try:
        old_file, new_file = None, None
        old_instance = sender.objects.get(pk=instance.pk)
        if hasattr(instance, "file_message"):
            old_file = old_instance.file_message
            new_file = instance.file_message

        if old_file != new_file or bool(old_file) != bool(new_file):
            # File has been updated or uploaded for the first time
            if old_file:
                # File was updated
                file_field_updated = True
            else:
                # New file uploaded
                file_field_updated = True
    except Exception as e:
        # New instance, file uploaded for the first time
        if hasattr(instance, "file_message") and instance.file_message:
            file_field_updated = True

    if file_field_updated:
        instance.url_serve = config("IMAGE_URL_SERVE")
        instance.file_upload_datetime = datetime.datetime.now()
