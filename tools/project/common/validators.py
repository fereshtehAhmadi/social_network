from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,11}$', message="Phone number is not valid.")

slug_regex = RegexValidator(regex=r"^[0-9a-z]*$", message="slug is not valid.")
