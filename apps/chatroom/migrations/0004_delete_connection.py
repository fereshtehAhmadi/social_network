# Generated by Django 5.0.6 on 2024-07-05 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chatroom", "0003_rename_customer_profile_chatroom_customer_newmessage"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Connection",
        ),
    ]