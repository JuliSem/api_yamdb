from django.db import models


class Category(models.Model):
    """Категории."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )


class Genre(models.Model):
    """Жанры."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
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