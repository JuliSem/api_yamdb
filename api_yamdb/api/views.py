from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken


from .filters import TitleFilter
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorModeratorAdminOrReadOnly
)
from .serializers import (
    CustomUserSerializer,
    ProfileEditSerializer,
    SignUpSerializer,
    TokenSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReadOnlyTitleSerializer,
    ReviewSerializer,
    CommentSerializer
)
from .mixins import ReviewViewSet
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from users.models import User
from reviews.models import Category, Genre, Title, Review


class UserViewSet(ModelViewSet):
    """Viewset для пользователя."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdmin, )
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=(IsAuthenticated, ))
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'PATCH':
            serializer = ProfileEditSerializer(request.user,
                                               data=request.data,
                                               partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Регистрация пользователя и отправка кода подтверждения."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(username=request.data['username'],
                                             email=request.data['email'])
    except IntegrityError:
        raise ValidationError('Неверное сочетание имени пользователя и email')
    confirmation_code = default_token_generator.make_token(user)
    send_mail('Подтверждение регистрации на сайте Yamdb!',
              f'Ваш код: {confirmation_code} для подтверждения регистрации',
              DEFAULT_FROM_EMAIL,
              [user.email],
              fail_silently=False)
    return Response({'email': user.email,
                     'username': user.username},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """Получение токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])
    confirmation_code = request.data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        respone = {'token': str(token)}
        return Response(respone, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(ReviewViewSet):
    """Вьюсет для создания обьектов "Категории"."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ReviewViewSet):
    """Вьюсет для создания обьектов "Жанры"."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов "Произведения"."""
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Для работы с отзывами."""
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorModeratorAdminOrReadOnly,
    ]

    def get_title(self):
        """Получение произведения."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title

    def get_queryset(self):
        title = self.get_title()
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Для работы с комментами."""
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorModeratorAdminOrReadOnly,
    ]

    def get_review(self):
        """Получение отзыва."""
        title__id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title__id=title__id, id=review_id)
        return review

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()
