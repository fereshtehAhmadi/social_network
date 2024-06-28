from django.contrib import admin

from apps.chatroom.models import ChatRoom, Message, Connection
from tools.django.admin import RelatedFieldAdminMixin, BaseModelAdmin


@admin.register(Connection)
class ConnectionAdmin(RelatedFieldAdminMixin, BaseModelAdmin):
    list_display = [
        "id",
        "customer__pk",
        "connection__pk",
        "accepted",
    ]
    search_fields = ['id', 'customer__pk']
    list_filter = ['accepted']
    autocomplete_fields = ["customer", "connection"]


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
