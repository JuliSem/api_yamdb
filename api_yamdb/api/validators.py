import re

from rest_framework.validators import ValidationError


def validate_username(value):
    """Валидация данных в поле username."""
    if value == 'me':
        raise ValidationError('Недопустимое имя для пользователя!')
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError('Имя пользователя содержит '
                              'запрещённые символы!')
