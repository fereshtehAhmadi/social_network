from apps.sms.models import SmsServicePanel, PatternSmsText
from apps.sms.tasks import mediana_sms_creation_task
from tools.django.django_tools import get_dynamic_attr
from tools.project.common.constants.model_cons import SmsServicePanelNameChoices


class SmsCreatorService:

    def __init__(self, service_panel: str = None, sms_error_object=None):
        """
        @param service_panel: name of sms panel : MED, PSH, default value is MED
        @param sms_error_object: object of SmsTaskErrorLog
        """
        self.service_panel = service_panel
        self.sms_error_object = sms_error_object

    sms_panels_tasks = {
        SmsServicePanelNameChoices.MEDIANA.value: mediana_sms_creation_task,
    }

    def find_sms_panel(self):
        service_panel = self.service_panel
        if not service_panel:
            service_panel = get_dynamic_attr(
                SmsServicePanel.objects.filter(is_active=True, main_panel=True).first(), 'name')

        return service_panel

    def find_pattern_sms(self, name, service_panel):
        pattern_sms = PatternSmsText.objects.filter(name=name, service_panel__name=service_panel)
        if not pattern_sms.exists():
            pattern_sms = PatternSmsText.objects.filter(name=name)

        return pattern_sms

    def __call__(self, sms_data: list = None, *args, **kwargs):
        service_panel = self.find_sms_panel()

        if sms_data is None:
            sms_data = list()
        elif isinstance(sms_data, dict):
            sms_data = list(sms_data)

        for user_sms_data in sms_data:
            if not kwargs.get("sms_type"):
                pattern_sms_name = user_sms_data.pop("sms_type")
            else:
                pattern_sms_name = kwargs.get("sms_type")

            pattern_sms = self.find_pattern_sms(name=pattern_sms_name, service_panel=service_panel)

            if pattern_sms.exists():
                service_panel = pattern_sms.first().service_panel.name
                if not self.sms_error_object:
                    self.sms_panels_tasks.get(service_panel).delay(
                        pattern_sms_id=pattern_sms.first().pk, sms_data=user_sms_data
                    )
                else:
                    self.sms_panels_tasks.get(service_panel).apply_async(
                        [
                            pattern_sms.first().pk,
                            user_sms_data,
                            get_dynamic_attr(self.sms_error_object, "id", None),
                        ],
                        countdown=self.sms_error_object.pattern_sms_text.resend_delay_time,
                    )
            else:
                print("pattern_sms does not exist")
