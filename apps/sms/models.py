from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q

from apps.base.models import BaseModel
from tools.project.common.constants.model_cons import SmsServicePanelNameChoices


class SmsServicePanel(BaseModel):
    name = models.CharField(
        max_length=3,
        choices=SmsServicePanelNameChoices.choices,
        unique=True
    )
    priority = models.IntegerField(default=0)
    main_panel = models.BooleanField(default=False)

    class Meta:
        verbose_name = "SmsService Panel"
        verbose_name_plural = "SmsService Panel"
        default_related_name = "sms_service_panels"

    def __str__(self):
        return self.get_name_display()


class PatternSmsText(BaseModel):
    service_panel = models.ForeignKey(
        SmsServicePanel,
        on_delete=models.PROTECT,
    )
    pattern_code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    text_message = models.TextField(
        max_length=2000,
        null=True,
        blank=True,
        help_text="sms text message that is sent",
    )
    description = models.TextField(
        max_length=2000,
        help_text="sms target and usage description",
        null=True,
        blank=True,
    )
    values_order = ArrayField(
        models.CharField(max_length=100),
        blank=True, default=list
    )
    has_resend_on_failure = models.BooleanField(default=False)
    resend_try_number = models.IntegerField(default=2)
    resend_delay_time = models.IntegerField(default=30, help_text="in second")
    has_sms_log = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Pattern Sms Text"
        verbose_name_plural = "Pattern Sms Text"
        default_related_name = "pattern_sms_texts"
        constraints = [
            models.UniqueConstraint(
                fields=["pattern_code", "service_panel"],
                condition=Q(is_active=True),
                name="pattern_sms_text_active_pattern_code",
            ),
            models.UniqueConstraint(
                fields=["name", "service_panel"],
                condition=Q(is_active=True),
                name="pattern_sms_text_active_name",
            ),
        ]

    def __str__(self):
        return "--".join([self.service_panel.name, self.name, self.pattern_code])


class SmsTaskErrorLog(BaseModel):
    pattern_sms_text = models.ForeignKey(
        PatternSmsText,
        on_delete=models.CASCADE,
        related_query_name="sms_task_error_log",
    )
    sent_data = models.JSONField()
    resend_count = models.IntegerField(default=0)
    successful_resend = models.BooleanField(default=False)
    panel_response = models.JSONField(null=True, blank=True)
    panel_response_status_code = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(null=True, blank=True, max_length=11)

    class Meta:
        verbose_name = "Sms Task Error Log"
        verbose_name_plural = "Sms Task Error Log"
        default_related_name = "sms_task_error_logs"


class SmsTaskLog(BaseModel):
    pattern_sms_text = models.ForeignKey(
        PatternSmsText,
        on_delete=models.CASCADE,
    )
    sent_data = models.JSONField()
    is_successful = models.BooleanField(default=True)
    panel_response = models.JSONField(null=True, blank=True)
    panel_response_status_code = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(null=True, blank=True, max_length=11)

    class Meta:
        verbose_name = "Sms Task Log"
        verbose_name_plural = "Sms Task Log"
        default_related_name = "sms_task_logs"
