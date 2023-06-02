from django.contrib import admin

from posts.models import Post, Image


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Класс для работы с постами в админ-панели."""

    list_display = ('pk', 'text', 'author', 'pub_date', 'update_date', )
    search_fields = ('text',)
    list_filter = ('pub_date',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Класс для работы с изображениями в админке."""

    list_display = ('pk', 'image_link', 'post',)
    search_fields = ('post',)
