# Generated by Django 5.0.6 on 2024-06-27 16:47

import django.db.models.deletion
import tools.project.common.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0003_alter_customerprofile_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customerprofile",
            name="slug",
            field=models.CharField(
                blank=True,
                max_length=15,
                null=True,
                unique=True,
                validators=[],
            ),
        ),
        migrations.AlterField(
            model_name="customerprofile",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                unique=True,
            ),
        ),
    ]
