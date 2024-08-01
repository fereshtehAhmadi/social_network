from django.apps import AppConfig


class ChatroomConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.chatroom"

    def ready(self):
        import apps.chatroom.signals
