from django.contrib import admin

from apps.chatroom.models import ChatRoom, Message, NewMessage
from tools.django.admin import RelatedFieldAdminMixin, BaseModelAdmin


@admin.register(NewMessage)
class NewMessageAdmin(RelatedFieldAdminMixin, BaseModelAdmin):
    list_display = [
        "id",
        "customer__pk",
        "new_messages",
    ]
    search_fields = ['id', 'customer__user__phone_number']
    autocomplete_fields = ["customer"]


@admin.register(ChatRoom)
class InsuranceOrderFlowAdmin(RelatedFieldAdminMixin, BaseModelAdmin):
    list_display = [
        "id",
        "sender__pk",
        "receiver__pk",
        "new_messages",
    ]
    search_fields = ['id', 'sender__user__phone_number']
    autocomplete_fields = ["sender", "receiver"]


@admin.register(Message)
class InsuranceOrderFlowAdmin(RelatedFieldAdminMixin, BaseModelAdmin):
    list_display = [
        "id",
        "sender__user__pk",
        "receiver__user__pk",
        # "chat_room__pk"
        "seen",
    ]
    search_fields = ['id', 'customer_profile__user__phone_number']
    autocomplete_fields = ["sender", "receiver", ]
