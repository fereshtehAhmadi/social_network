# Generated by Django 5.0.6 on 2024-06-25 20:56

import apps.chatroom.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChatRoom",
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
                ("new_messages", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "Chat Room",
                "verbose_name_plural": "Chat Room",
                "default_related_name": "chat_rooms",
            },
        ),
        migrations.CreateModel(
            name="Message",
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
                ("message", models.TextField(blank=True, null=True)),
                (
                    "file_message",
                    models.FileField(
                        blank=True,
                        max_length=500,
                        null=True,
                        upload_to=apps.chatroom.models.Message.file_message_path,
                    ),
                ),
                ("seen", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Message",
                "verbose_name_plural": "Message",
                "default_related_name": "messages",
            },
        ),
    ]
