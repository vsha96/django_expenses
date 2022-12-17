from django.core.exceptions import ValidationError


def validate_money(value):
    if value <= 0:
        raise ValidationError(
            ('Ticket money must be > 0'),
            params={'value': value},)