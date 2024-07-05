# Generated by Django 5.0.6 on 2024-07-05 09:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatroom", "0002_initial"),
        ("profiles", "0002_alter_adminprofile_user_alter_customerprofile_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="chatroom",
            old_name="customer_profile",
            new_name="customer",
        ),
        migrations.CreateModel(
            name="NewMessage",
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
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.customerprofile",
                    ),
                ),
            ],
            options={
                "verbose_name": "New Message",
                "verbose_name_plural": "New Message",
                "default_related_name": "new_messages",
            },
        ),
    ]