from django.contrib.auth import get_user_model #  будет в user/models.py
from rest_framework.validators import ValidationError


User = get_user_model() #  будет переопределено в user/models.py

def validate_username(value):
    if value == 'me':
        raise ValidationError('Недопустимое имя для пользователя!')
    elif User.objects.filter(username=value).exists():
        raise ValidationError('Пользователь с таким именем '
                              'уже существует!')
    
def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('Пользователь с такой электронной почтой '
                              'уже зарегистрирован!')