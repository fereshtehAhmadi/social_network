# Generated by Django 5.0.6 on 2024-08-06 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatroom", "0006_message_url_serve"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="seen",
            field=models.BooleanField(default=False),
        ),
    ]
