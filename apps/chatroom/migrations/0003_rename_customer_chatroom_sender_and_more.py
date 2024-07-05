# Generated by Django 5.0.6 on 2024-07-05 13:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatroom", "0002_initial"),
        ("profiles", "0002_alter_customerprofile_public"),
    ]

    operations = [
        migrations.RenameField(
            model_name="chatroom",
            old_name="customer",
            new_name="sender",
        ),
        migrations.RemoveField(
            model_name="chatroom",
            name="connection",
        ),
        migrations.AddField(
            model_name="chatroom",
            name="receiver",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="chatroom_receiver",
                to="profiles.customerprofile",
            ),
        ),
    ]
