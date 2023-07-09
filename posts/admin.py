from django.contrib import admin

from config.settings import PAGINATION_LIMIT_IN_ADMIN_PANEL
from posts.models import Image, Post, Comment

admin.site.site_title = 'Корпоративная сеть'
admin.site.site_header = 'Корпоративная сеть'
admin.site.index_title = 'Администрирование'


class ImageInline(admin.TabularInline):
    """Отображение картинки на странице поста."""

    model = Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Класс для работы с изображениями в админке."""

    list_display = ('pk', 'image_link', 'post',)
    search_fields = ('post',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Класс для работы с постами в админ-панели."""

    list_display = (
        'pk', 'author', 'text', 'pub_date', 'update_date',
        'get_likes_count', 'get_comments_count',
    )
    list_display_links = ('text',)
    search_fields = ('text',)
    list_filter = ('pub_date', 'author')
    ordering = ('-pub_date',)
    inlines = (ImageInline,)
    empty_value_display = '-пусто-'
    list_per_page = PAGINATION_LIMIT_IN_ADMIN_PANEL

    @admin.display(description='Количество лайков')
    def get_likes_count(self, obj):
        return obj.likes.count()

    @admin.display(description='Количество комментов')
    def get_comments_count(self, obj):
        return obj.comments.count()


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'text', 'post', 'pub_date', 'get_likes_count',
    )
    list_display_links = ('author',)
    search_fields = ('text',)
    list_filter = ('pub_date', 'author')
    ordering = ('-pub_date',)
    empty_value_display = '-пусто-'
    list_per_page = PAGINATION_LIMIT_IN_ADMIN_PANEL

    @admin.display(description='Количество лайков')
    def get_likes_count(self, obj):
        return obj.like.count()
