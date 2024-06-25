from django.db.models.signals import post_save
from django.dispatch import receiver

from tools.project.common.constants.model_cons import SmsServicePanelNameChoices
from tools.project.sms.service import SmsCreatorService
from .models import SmsServicePanel, SmsTaskErrorLog


@receiver(post_save, sender=SmsTaskErrorLog)
def sms_retry_post_save(sender, instance, created, **kwargs):
    if (
        instance.pattern_sms_text.has_resend_on_failure is True
        and instance.successful_resend is False
    ):
        if instance.resend_count < instance.pattern_sms_text.resend_try_number:
            if instance.panel_response_status_code in range(500, 600):
                if instance.pattern_sms_text.service_panel.name == SmsServicePanelNameChoices.PISHGAMRAYAN:
                    SmsCreatorService(service_panel=SmsServicePanelNameChoices.MEDIANA,
                                      sms_error_object=instance).__call__(sms_data=[instance.sent_data],
                                                                          sms_type=instance.pattern_sms_text.name)

                elif instance.pattern_sms_text.service_panel.name == SmsServicePanelNameChoices.MEDIANA:
                    SmsCreatorService(service_panel=SmsServicePanelNameChoices.PISHGAMRAYAN,
                                      sms_error_object=instance).__call__(sms_data=[instance.sent_data],
                                                                          sms_type=instance.pattern_sms_text.name)
                else:
                    SmsCreatorService(service_panel=instance.pattern_sms_text.service_panel.name,
                                      sms_error_object=instance).__call__(sms_data=[instance.sent_data],
                                                                          sms_type=instance.pattern_sms_text.name)
            else:
                SmsCreatorService(service_panel=instance.pattern_sms_text.service_panel.name,
                                  sms_error_object=instance).__call__(sms_data=[instance.sent_data],
                                                                      sms_type=instance.pattern_sms_text.name)


@receiver(post_save, sender=SmsServicePanel)
def sms_service_panel_post_save(sender, instance, **kwargs):
    main = SmsServicePanel.objects.filter(main_panel=True).exclude(id=instance.id)
    if main and instance.main_panel is True:
        main = main.first()
        main.main_panel = False
        main.save()
        instance.main_panel = True
