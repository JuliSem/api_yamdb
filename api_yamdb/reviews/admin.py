from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_genres')
    list_editable = ('category',)

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])


admin.site.register(Title, TitleAdmin)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Genre)
