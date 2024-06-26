from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,11}$', message="Phone number is not valid.")

slug_regex = RegexValidator(regex=r"^[_0-9a-z_]*$", message="slug is not valid.")
