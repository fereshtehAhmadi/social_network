# Generated by Django 5.0.6 on 2024-07-05 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("account", "0001_initial"),
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="connection",
            name="receiver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="connection_receiver",
                to="profiles.customerprofile",
            ),
        ),
        migrations.AddField(
            model_name="connection",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="connection_sender",
                to="profiles.customerprofile",
            ),
        ),
    ]
