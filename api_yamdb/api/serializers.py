from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import ValidationError
from datetime import datetime

from .validators import validate_username
from users.models import User
from reviews.models import Category, Genre, Title, Review, Comment


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


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели "Произведения"."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при небезопасных запросах."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > int(datetime.now().year):
            raise serializers.ValidationError(
                'Значение года не может быть больше текущего!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для отзывы."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        if request.method == 'PATCH':
            return data

        user = self.context['request'].user
        title_id = request.parser_context['kwargs']['title_id']

        if Review.objects.filter(author=user, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение'
            )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для коммента."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment
