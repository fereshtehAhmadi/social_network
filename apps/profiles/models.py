import random

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.base.models import BaseModel
from apps.profiles.user_managers import CustomUserManager
from tools.project.common.validators import phone_regex


class User(BaseModel, AbstractUser):
    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        verbose_name=_("phone_number"),
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True, null=True)

    STR_RETURN_LIST = ["pk", "phone_number"]
    UNIQUE_CHECK_LIST = [("shared_user_id", Q(shared_user_id__isnull=False))]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        default_related_name = "users"


class CustomerProfile(BaseModel):
    def customer_profile_avatar_path(self, filename):
        return "customer_profile/{0}/avatar/{1}".format(
            str(self.user.id),
            "_".join([str(random.randint(1000000000, 9999999999)), filename]),
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(
        max_length=500,
        null=True, blank=True,
        upload_to=customer_profile_avatar_path,
    )
    bio = models.TextField(null=True, blank=True)
    public = models.BooleanField(default=True)

    STR_RETURN_LIST = ["pk", "user__id"]
    UNIQUE_CHECK_LIST = [('user', Q())]

    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profile"
        default_related_name = "customer_profiles"

    @property
    def get_dynamic_url(self):
        if self.avatar:
            return f"{settings.IMAGE_URL_SERVE}{settings.MEDIA_URL}{self.avatar}"
        else:
            return None


class AdminProfile(BaseModel):
    def admin_profile_avatar_path(self, filename):
        return "customer_profile/{0}/avatar/{1}".format(
            str(self.user.pk),
            "_".join([str(random.randint(1000000000, 9999999999)), filename]),
        )

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.FileField(
        max_length=500,
        null=True, blank=True,
        upload_to=admin_profile_avatar_path,
    )

    STR_RETURN_LIST = ["pk", "user__id"]
    UNIQUE_CHECK_LIST = [("user", Q())]

    class Meta:
        verbose_name = "Admin Profile"
        verbose_name_plural = "Admin Profile"
        default_related_name = "admin_profiles"

    @property
    def get_dynamic_url(self):
        if self.avatar:
            return f"{settings.IMAGE_URL_SERVE}{settings.MEDIA_URL}{self.avatar}"
        else:
            return None
