from django.contrib import admin

from posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Класс для работы с постами в админ-панели."""

    list_display = ('pk', 'text', 'author', 'pub_date', 'update_date', 'image',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
