# Generated by Django 5.0.6 on 2024-07-05 12:33

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SmsServicePanel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("creation_datetime", models.DateTimeField(auto_now_add=True)),
                ("update_datetime", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(
                        choices=[("MED", "مدیانا")], max_length=3, unique=True
                    ),
                ),
                ("priority", models.IntegerField(default=0)),
                ("main_panel", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "SmsService Panel",
                "verbose_name_plural": "SmsService Panel",
                "default_related_name": "sms_service_panels",
            },
        ),
        migrations.CreateModel(
            name="PatternSmsText",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("creation_datetime", models.DateTimeField(auto_now_add=True)),
                ("update_datetime", models.DateTimeField(auto_now=True)),
                ("pattern_code", models.CharField(max_length=100)),
                ("name", models.CharField(max_length=100)),
                (
                    "text_message",
                    models.TextField(
                        blank=True,
                        help_text="sms text message that is sent",
                        max_length=2000,
                        null=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="sms target and usage description",
                        max_length=2000,
                        null=True,
                    ),
                ),
                (
                    "values_order",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                ("has_resend_on_failure", models.BooleanField(default=False)),
                ("resend_try_number", models.IntegerField(default=2)),
                (
                    "resend_delay_time",
                    models.IntegerField(default=30, help_text="in second"),
                ),
                ("has_sms_log", models.BooleanField(default=False)),
                (
                    "service_panel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="sms.smsservicepanel",
                    ),
                ),
            ],
            options={
                "verbose_name": "Pattern Sms Text",
                "verbose_name_plural": "Pattern Sms Text",
                "default_related_name": "pattern_sms_texts",
            },
        ),
        migrations.CreateModel(
            name="SmsTaskErrorLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("creation_datetime", models.DateTimeField(auto_now_add=True)),
                ("update_datetime", models.DateTimeField(auto_now=True)),
                ("sent_data", models.JSONField()),
                ("resend_count", models.IntegerField(default=0)),
                ("successful_resend", models.BooleanField(default=False)),
                ("panel_response", models.JSONField(blank=True, null=True)),
                (
                    "panel_response_status_code",
                    models.IntegerField(blank=True, null=True),
                ),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=11, null=True),
                ),
                (
                    "pattern_sms_text",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_query_name="sms_task_error_log",
                        to="sms.patternsmstext",
                    ),
                ),
            ],
            options={
                "verbose_name": "Sms Task Error Log",
                "verbose_name_plural": "Sms Task Error Log",
                "default_related_name": "sms_task_error_logs",
            },
        ),
        migrations.CreateModel(
            name="SmsTaskLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("creation_datetime", models.DateTimeField(auto_now_add=True)),
                ("update_datetime", models.DateTimeField(auto_now=True)),
                ("sent_data", models.JSONField()),
                ("is_successful", models.BooleanField(default=True)),
                ("panel_response", models.JSONField(blank=True, null=True)),
                (
                    "panel_response_status_code",
                    models.IntegerField(blank=True, null=True),
                ),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=11, null=True),
                ),
                (
                    "pattern_sms_text",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sms.patternsmstext",
                    ),
                ),
            ],
            options={
                "verbose_name": "Sms Task Log",
                "verbose_name_plural": "Sms Task Log",
                "default_related_name": "sms_task_logs",
            },
        ),
        migrations.AddConstraint(
            model_name="patternsmstext",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_active", True)),
                fields=("pattern_code", "service_panel"),
                name="pattern_sms_text_active_pattern_code",
            ),
        ),
        migrations.AddConstraint(
            model_name="patternsmstext",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_active", True)),
                fields=("name", "service_panel"),
                name="pattern_sms_text_active_name",
            ),
        ),
    ]
