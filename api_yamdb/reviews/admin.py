
from django.contrib import admin

from api_yamdb import settings

from reviews.models import Category, Comment, Genre, Review, Title

admin.site.register(Comment)
admin.site.register(Review)


class CategoryAdmin(admin.ModelAdmin):
    """Класс настройки раздела категорий."""

    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = '-пусто-'
    list_filter = ('name',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class GenreAdmin(admin.ModelAdmin):
    """Класс настройки раздела жанров."""

    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = '-пусто-'
    list_filter = ('name',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Genre, GenreAdmin)


class GenreshipInline(admin.TabularInline):
    """Класс для получения списка жанров."""

    model = Title.genre.through


class TitleAdmin(admin.ModelAdmin):
    """Класс настройки раздела произведений."""

    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        'get_genre',
        'count_reviews',
        'get_rating'
    )
    empty_value_display = '-пусто-'
    list_filter = ('name',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('name', 'year', 'category')
    list_editable = ('category',)
    inlines = (GenreshipInline,)

    def count_reviews(self, object):
        """Вычисляет количество отзывов на произведение."""
        return object.reviews.count()

    count_reviews.short_description = 'Количество отзывов'


admin.site.register(Title, TitleAdmin)
