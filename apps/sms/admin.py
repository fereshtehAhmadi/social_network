from django import forms
from django.contrib import admin

from .models import SmsServicePanel, SmsTaskErrorLog, SmsTaskLog, PatternSmsText
from tools.django.admin import BaseModelAdmin, RelatedFieldAdminMixin


@admin.register(SmsServicePanel)
class SmsServicePanelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "priority", "is_active", "main_panel"]
    search_fields = ['name']


@admin.register(SmsTaskErrorLog)
class SmsTaskErrorLogAdmin(RelatedFieldAdminMixin, BaseModelAdmin):
    list_display = ['id', 'is_active', 'resend_count', 'successful_resend', 'panel_response_status_code',
                    'pattern_sms_text__service_panel__name', 'pattern_sms_text__name']
    search_fields = ['pattern_sms_text__name', 'phone_number']
    readonly_fields = ['pattern_sms_text', 'sent_data', 'panel_response']
    autocomplete_fields = ['pattern_sms_text']


@admin.register(SmsTaskLog)
class SmsTaskLogAdmin(RelatedFieldAdminMixin, BaseModelAdmin):
    list_display = ['id', 'panel_response_status_code', 'pattern_sms_text__service_panel__name',
                    'pattern_sms_text__name', 'is_successful']
    search_fields = ['pattern_sms_text__name', 'phone_number']
    readonly_fields = ['pattern_sms_text', 'sent_data', 'panel_response']
    list_filter = ['is_successful', 'pattern_sms_text__service_panel__name']
    autocomplete_fields = ['pattern_sms_text']


class PatternSmsTextAdminForm(forms.ModelForm):
    values_order_1 = forms.CharField(
        required=False,
        min_length=1,
        max_length=100,
    )
    values_order_2 = forms.CharField(
        required=False,
        min_length=1,
        max_length=100,
    )
    values_order_3 = forms.CharField(
        required=False,
        min_length=1,
        max_length=100,
    )
    values_order_4 = forms.CharField(
        required=False,
        min_length=1,
        max_length=100,
    )
    values_order_5 = forms.CharField(
        required=False,
        min_length=1,
        max_length=100,
    )
    values_order_6 = forms.CharField(
        required=False,
        min_length=1,
        max_length=100,
    )
    values_order_7 = forms.CharField(
        required=False,
        min_length=1,
        max_length=100,
    )
    values_order_8 = forms.CharField(
        required=False,
        min_length=1,
        max_length=100,
    )
    values_order_9 = forms.CharField(
        required=False,
        min_length=1,
        max_length=100,
    )
    values_order_10 = forms.CharField(
        required=False,
        min_length=1,
        max_length=100,
    )
    values_order_11 = forms.CharField(
        required=False,
        min_length=1,
        max_length=100,
    )
    values_order_12 = forms.CharField(
        required=False,
        min_length=1,
        max_length=100,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get instance of CompanyAppInformation
        instance = kwargs.get("instance")
        if instance:
            # Populate description fields with values from the 'description' field
            values_order = instance.values_order or []
            for index, value in enumerate(values_order, start=1):
                field_name = f"values_order_{index}"
                if field_name in self.fields:
                    self.fields[field_name].initial = value

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Extract values from separate fields and update the description
        values_order = [
            self.cleaned_data[f"values_order_{index}"]
            for index in range(1, 13)
            if f"values_order_{index}" in self.cleaned_data
               and self.cleaned_data[f"values_order_{index}"]
        ]
        instance.values_order = values_order
        if commit:
            instance.save()
        return instance

    class Meta:
        model = PatternSmsText
        fields = "__all__"


@admin.register(PatternSmsText)
class PatternSmsTextAdmin(RelatedFieldAdminMixin, BaseModelAdmin):
    list_display = [
        "id",
        "service_panel",
        "pattern_code",
        "name",
        "description",
        "is_active",
    ]
    list_display_links = ["id", "service_panel"]
    list_filter = ["service_panel", "is_active"]
    search_fields = ["pattern_code", "name", "text_message"]
    form = PatternSmsTextAdminForm
    readonly_fields = ["values_order"]
    list_editable = ["pattern_code"]
    autocomplete_fields = ['service_panel']
