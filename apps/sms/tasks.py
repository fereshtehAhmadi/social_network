import base64
import json

import requests
from celery import shared_task
from decouple import config

from apps.sms.models import PatternSmsText, SmsTaskLog, SmsTaskErrorLog


def create_sms_log(sms_data, pattern_sms_text, panel_response, sms_error_object_id, **kwargs):
    # create sms log for patterns with has_sms_log=True
    if pattern_sms_text.has_sms_log is True:
        SmsTaskLog.objects.create(pattern_sms_text=pattern_sms_text, sent_data=sms_data,
                                  panel_response=panel_response.json(),
                                  is_successful=True if panel_response.status_code in range(200, 300) else False,
                                  panel_response_status_code=panel_response.status_code,
                                  phone_number=sms_data.get('phone_number'))

    # check sms panel request response for sms error log creation
    if panel_response.status_code not in range(200, 300):
        if sms_error_object_id is None:  # create a new error log
            SmsTaskErrorLog.objects.create(pattern_sms_text=pattern_sms_text, sent_data=sms_data,
                                           panel_response=panel_response.json(),
                                           panel_response_status_code=panel_response.status_code,
                                           phone_number=sms_data.get('phone_number'))
        else:  # update error log with another failed response
            sms_error_object = SmsTaskErrorLog.objects.get(pk=sms_error_object_id)
            sms_error_object.resend_count += 1
            sms_error_object.panel_response = panel_response.json()
            sms_error_object.save()

    else:  # update error log with successful response
        if sms_error_object_id is not None:
            sms_error_object = SmsTaskErrorLog.objects.get(pk=sms_error_object_id)
            sms_error_object.resend_count += 1
            sms_error_object.successful_resend = True
            sms_error_object.save()


@shared_task()
def mediana_sms_creation_task(pattern_sms_id, sms_data, sms_error_object_id=None):
    url = config("MEDIANA_URL")
    username, password = config("USERNAME_MEDIANA"), config("PASSWORD_MEDIANA")
    api_key = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode()
    headers = {"Content-Type": "application/json", "Authorization": f"Basic {api_key}"}

    pattern_sms_text = PatternSmsText.objects.get(pk=pattern_sms_id)
    phone_number = ["98" + sms_data["phone_number"][1:]]
    print(
        f"phone_number : {phone_number[0]}       type : {pattern_sms_text.name}        panel : mediana"
    )

    values_order = pattern_sms_text.values_order
    values = []
    for v in values_order:
        values.append(sms_data.get(v))

    payload = {
        "Destinations": phone_number,
        "Parameters": values,
        "PatternId": pattern_sms_text.pattern_code,
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(response)

    create_sms_log(
        sms_data=sms_data,
        pattern_sms_text=pattern_sms_text,
        panel_response=response,
        sms_error_object_id=sms_error_object_id,
    )

