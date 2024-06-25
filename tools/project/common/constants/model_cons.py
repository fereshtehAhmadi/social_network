from django.db.models import TextChoices


class UserRoleChoice(TextChoices):
    CUSTOMER = "customer", "مشتری"
    ADMIN = "admin", "مدیر سامانه"


class SmsServicePanelNameChoices(TextChoices):
    MEDIANA = "MED", "مدیانا"