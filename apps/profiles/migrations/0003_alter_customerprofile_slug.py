# Generated by Django 5.0.6 on 2024-06-27 16:35

import tools.project.common.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0002_alter_customerprofile_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customerprofile",
            name="slug",
            field=models.CharField(
                blank=True,
                max_length=15,
                null=True,
                validators=[],
            ),
        ),
    ]