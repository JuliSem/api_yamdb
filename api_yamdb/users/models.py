from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import validate_username


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    CHOICES = (
        (USER, 'Аутентифицированный пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор')
    )
    username = models.CharField(verbose_name='Пользователь',
                                validators=(validate_username,),
                                max_length=150,
                                unique=True)
    first_name = models.CharField(verbose_name='Имя',
                                  max_length=150,
                                  blank=True)
    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=150,
                                 blank=True)
    email = models.EmailField(verbose_name='Электронная почта',
                              max_length=254,
                              unique=True)
    bio = models.TextField(verbose_name='Биография',
                           blank=True)
    role = models.CharField(verbose_name='Пользовательская роль',
                            max_length=50,
                            choices=CHOICES,
                            default=USER)

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR
