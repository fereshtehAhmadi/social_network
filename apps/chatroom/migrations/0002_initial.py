# Generated by Django 5.0.6 on 2024-07-05 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("chatroom", "0001_initial"),
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatroom",
            name="connection",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="chatroom_connections",
                to="profiles.customerprofile",
            ),
        ),
        migrations.AddField(
            model_name="chatroom",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="profiles.customerprofile",
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="chat_room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="chatroom.chatroom"
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="receiver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="receiver_messages",
                to="profiles.customerprofile",
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="sender_messages",
                to="profiles.customerprofile",
            ),
        ),
        migrations.AddField(
            model_name="newmessage",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="profiles.customerprofile",
            ),
        ),
    ]
