from django.contrib.auth import get_user_model # будет в user/models.py
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import ValidationError

from api.validators import validate_email, validate_username

User = get_user_model() #  будет переопределено в user/models.py


class SignUpSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=150,
                                     allow_blank=False,
                                     validators=[validate_username])
    email = serializers.EmailField(max_length=254,
                                   allow_blank=False,
                                   validators=[validate_email])

    class Meta:
        fields = ('username', 'email', )
        model = User



class TokenSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=150,
                                     allow_blank=False,
                                     validators=[validate_username])
    confirmation_code = serializers.CharField(allow_blank=False)

    class Meta:
        fields = ('username', 'confirmation_code', )
        model = User

        def validate(self, data):
            user = get_object_or_404(User, username=data['username'])
            confirmation_code = default_token_generator.make_token(user)
            if str(confirmation_code) != data['confirmation_code']:
                raise ValidationError('Введен неверный код подтверждения!')
            return data
