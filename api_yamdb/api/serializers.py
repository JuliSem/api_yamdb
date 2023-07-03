from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import ValidationError
from datetime import datetime

from api.validators import validate_username
from users.models import User
from reviews.models import Category, Genre, Title


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


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели "Категории"."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели "Жанры"."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели "Произведения"."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        if value > int(datetime.now().year):
            raise serializers.ValidationError(
                'Значение года не может быть больше текущего!'
            )
        return value
