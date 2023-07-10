from django.db import models
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator
)
from django.conf import settings
from datetime import datetime


from api_yamdb.constants import (
    MIN_SCORE,
    MAX_SCORE,
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH,
    RESTRICT_NAME
)


class ModelCategoryOrGenre(models.Model):
    """Абстрактная модель для жанров и категорий"""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name="Название"
    )
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='В слаге категории указан недопустимый символ'
        )]
    )

    class Meta:
        abstract = True


class Category(ModelCategoryOrGenre):
    """Категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)

    def __str__(self):
        return self.name[:RESTRICT_NAME]


class Genre(ModelCategoryOrGenre):
    """Жанры."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('id',)

    def __str__(self):
        return self.name[:RESTRICT_NAME]


class Title(models.Model):
    """Произведения."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name="Название"
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        validators=[
            MinValueValidator(
                0,
                message='Значение года не может быть отрицательным'
            ),
            MaxValueValidator(
                int(datetime.now().year),
                message='Значение года не может быть больше текущего'
            )
        ],
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='titles',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:RESTRICT_NAME]


class CreateMixin(models.Model):
    """Добавляет к модели дату публикации."""
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class Review(CreateMixin):
    """Отзыв."""
    text = models.TextField(verbose_name='Текст')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(MIN_SCORE, 'Оценка не может быть меньше 1'),
            MaxValueValidator(MAX_SCORE, 'Оценка не может быть выше 10')
        ]
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date', )
        unique_together = ('author', 'title')

    def __str__(self):
        return f'{self.title}, {self.score}, {self.author}'


class Comment(CreateMixin):
    """Комментарий."""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(verbose_name='Текст комментария')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.author}, {self.pub_date}: {self.text}'
