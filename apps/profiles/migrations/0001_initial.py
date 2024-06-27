# Generated by Django 5.0.6 on 2024-06-27 17:33

import apps.profiles.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("creation_datetime", models.DateTimeField(auto_now_add=True)),
                ("update_datetime", models.DateTimeField(auto_now=True)),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=17,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number is not valid.",
                                regex="^\\+?1?\\d{9,11}$",
                            )
                        ],
                        verbose_name="phone_number",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="last name"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
                "default_related_name": "users",
            },
        ),
        migrations.CreateModel(
            name="AdminProfile",
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
                (
                    "avatar",
                    models.FileField(
                        blank=True,
                        max_length=500,
                        null=True,
                        upload_to=apps.profiles.models.AdminProfile.admin_profile_avatar_path,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Admin Profile",
                "verbose_name_plural": "Admin Profile",
                "default_related_name": "admin_profiles",
            },
        ),
        migrations.CreateModel(
            name="CustomerProfile",
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
                (
                    "avatar",
                    models.FileField(
                        blank=True,
                        max_length=500,
                        null=True,
                        upload_to=apps.profiles.models.CustomerProfile.customer_profile_avatar_path,
                    ),
                ),
                ("bio", models.TextField(blank=True, null=True)),
                (
                    "slug",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="slug is not valid.", regex="^[_0-9a-z_]*$"
                            )
                        ],
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        unique=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Customer Profile",
                "verbose_name_plural": "Customer Profile",
                "default_related_name": "customer_profiles",
            },
        ),
    ]
