from django.core.exceptions import ValidationError


def phone_validator(number):
    if number.startswith('+'):
        return number
        
    return ValidationError("Phone number has to start with + ")
