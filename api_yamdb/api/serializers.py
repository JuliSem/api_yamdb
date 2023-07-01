from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import ValidationError

from api.validators import validate_username
from users.models import User


class SignUpSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150,
                                     required=True,
                                     validators=[validate_username])
    email = serializers.EmailField(max_length=254,
                                   required=True)


class TokenSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150,
                                     required=True,
                                     validators=[validate_username])
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = default_token_generator.make_token(user)
        if str(confirmation_code) != data['confirmation_code']:
            raise ValidationError('Введен неверный код подтверждения!')
        return data


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role', )
        model = User


class ProfileEditSerializer(CustomUserSerializer):
    role = serializers.CharField(read_only=True)
