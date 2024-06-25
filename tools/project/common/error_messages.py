from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ErrorMessagesCons(TextChoices):
    # basics
    message = "message", _("message")
    unique = "This field must be unique.", _("This field must be unique.")
    blank = "This field cannot be blank.", _("This field cannot be blank.")
    null = "This field cannot be null.", _("This field cannot be null.")
    does_not_exist = "Object does not exist.", _("Object does not exist.")
    required = "This field is required.", _("This field is required.")
    invalid = "This field is not valid.", _("This field is not valid.")
    token_not_valid = "Token is invalid or expired", _("Token is invalid or expired")
    username_unique = "A user with that username already exists.", _("A user with that username already exists.")


