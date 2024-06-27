# Generated by Django 5.0.6 on 2024-06-27 17:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0004_alter_customerprofile_slug_and_more"),
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
                validators=[
                    django.core.validators.RegexValidator(
                        message="slug is not valid.", regex="^[0-9]*$"
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(
                blank=True,
                max_length=17,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number is not valid.", regex="^\\+?1?\\d{9,11}$"
                    )
                ],
                verbose_name="phone_number",
            ),
        ),
    ]