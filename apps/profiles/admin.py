from django.contrib import admin

from apps.profiles.models import User, CustomerProfile, AdminProfile
from tools.django.admin import RelatedFieldAdminMixin, BaseModelAdmin


@admin.register(User)
class UserAdmin(RelatedFieldAdminMixin, BaseModelAdmin):
    list_display = [
        "id",
        "username",
        "phone_number",
    ]
    search_fields = ["id"]


@admin.register(CustomerProfile)
class CustomerProfileAdmin(RelatedFieldAdminMixin, BaseModelAdmin):
    list_display = [
        "id",
        "user",
        "public",
    ]
    search_fields = ["user__phone_number", ]
    autocomplete_fields = ["user"]


@admin.register(AdminProfile)
class AdminProfileAdmin(RelatedFieldAdminMixin, BaseModelAdmin):
    list_display = ["id", "user__phone_number", ]
    search_fields = ["user__phone_number", ]
    autocomplete_fields = ["user"]
