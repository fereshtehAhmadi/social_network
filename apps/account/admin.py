from django.contrib import admin

from apps.account.models import Connection
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
