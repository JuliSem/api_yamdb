from django.contrib.auth import get_user_model  # будет в  user/models.py
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import SignUpSerializer, TokenSerializer
from api_yamdb.settings import DEFAULT_FROM_EMAIL


User = get_user_model()  # будет переопределено в user/models.py


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Создание пользователя и отправка кода подтверждения."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if not User.objects.filter(username=request.data['username'],
                               email=request.data['email']):
        serializer.save()
    user = User.objects.get(username=request.data['username'],
                            email=request.data['email'])
    confirmation_code = default_token_generator.make_token(user)
    send_mail('Подтверждение регистрации на сайте Yamdb!',
              f'Ваш код: {confirmation_code} для подтверждения регистрации',
              DEFAULT_FROM_EMAIL,
              [user.email]
              )
    return Response(
        {'result': 'Код подтверждения успешно отправлен!'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """Получение и отправка токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])
    confirmation_code = request.data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        respone = {'token': str(token)}
        return Response(respone, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
