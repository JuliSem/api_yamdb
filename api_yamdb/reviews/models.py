from django.db import models
from django.core.validators import (RegexValidator, MinValueValidator,
                                    MaxValueValidator)
from django.conf import settings


class Category(models.Model):
    """Категории."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='В слаге категории указан недопустимый символ'
        )]
    )


class Genre(models.Model):
    """Жанры."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='В слаге жанра указан недопустимый символ'
        )]
    )


class Title(models.Model):
    """Произведения."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название"
    )
    year = models.IntegerField(
        verbose_name='Год выпуска'
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
        # Т.к. используем паджинатор, иначе получим
        ordering = ['-id']


class GenreTitle(models.Model):
    """Связь между жанром и произведением."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )


class Review(models.Model):
    """Отзыв."""
    text = models.TextField(verbose_name='Текст')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1'),
            MaxValueValidator(10, 'Оценка не может быть выше 10')
        ]
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        # Отзываы нужны сортированные по дате публикации.
        ordering = ['-pub_date']
        # Один отзыв для одного автора, не более.
        unique_together = ('author', 'title')

    def __str__(self):
        return f'{self.title}, {self.score}, {self.author}'


class Comment(models.Model):
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
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        # Комменты тоже нужны по дате пуликации.
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.author}, {self.pub_date}: {self.text}'