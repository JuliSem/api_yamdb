from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import ValidationError

from reviews.models import Review, Comment
from .validators import validate_username
from users.models import User


class SignUpSerializer(serializers.Serializer):
    """Serializer для регистрации пользователя."""

    username = serializers.CharField(max_length=150,
                                     required=True,
                                     validators=[validate_username])
    email = serializers.EmailField(max_length=254,
                                   required=True)


class TokenSerializer(serializers.Serializer):
    """Serializer для получения токена."""

    username = serializers.CharField(max_length=150,
                                     required=True,
                                     validators=[validate_username])
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            raise ValidationError('Введен неверный код подтверждения!')
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer для модели пользователя."""

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role', )
        model = User


class ProfileEditSerializer(CustomUserSerializer):
    """Serializer для редактирования данных пользователя."""
    role = serializers.CharField(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для отзывы."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        user = self.context['request'].user
        request = self.context['request']
        title_id = request.parser_context['kwargs']['title_id']

        if Review.objects.filter(author=user, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для коммента."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment