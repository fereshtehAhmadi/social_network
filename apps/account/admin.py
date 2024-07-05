from django.contrib import admin

from apps.account.models import Connection
from tools.django.admin import RelatedFieldAdminMixin, BaseModelAdmin


@admin.register(Connection)
class ConnectionAdmin(RelatedFieldAdminMixin, BaseModelAdmin):
    list_display = [
        "id",
        "sender__pk",
        "receiver__pk",
        "accepted",
    ]
    search_fields = ['id', 'receiver__pk']
    list_filter = ['accepted']
    autocomplete_fields = ["sender", "receiver"]
