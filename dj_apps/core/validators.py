from django.core.validators import RegexValidator

NumericValidator = RegexValidator(r"^[0-9]*$", "Only numeric characters are allowed.")
