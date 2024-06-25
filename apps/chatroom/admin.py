from django.contrib import admin

from apps.chatroom.models import ChatRoom, Message
from tools.django.admin import RelatedFieldAdminMixin, BaseModelAdmin


@admin.register(ChatRoom)
class InsuranceOrderFlowAdmin(RelatedFieldAdminMixin, BaseModelAdmin):
    list_display = [
        "id",
        "customer_profile__pk",
        "new_messages",
    ]
    search_fields = ['id', 'customer_profile__phone_number']
    autocomplete_fields = ["customer_profile"]


@admin.register(Message)
class InsuranceOrderFlowAdmin(RelatedFieldAdminMixin, BaseModelAdmin):
    list_display = [
        "id",
        "sender__user__pk",
        "receiver__user__pk",
        "seen",
    ]
    search_fields = ['id', 'customer_profile__phone_number']
    autocomplete_fields = ["sender", "receiver"]
