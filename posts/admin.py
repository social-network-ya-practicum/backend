from django.contrib import admin

from posts.models import Image, Post


class ImageInline(admin.TabularInline):
    """Отображение картинки на странице поста."""

    model = Image


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Класс для работы с постами в админ-панели."""

    list_display = ('pk', 'text', 'author', 'pub_date', 'update_date', )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    inlines = (ImageInline,)
    add_fieldsets = (
        (None, {'fields': ('count_likes', ), }),
    )

    def count_likes(self, obj):
        return obj.users_like.count()

    count_likes.short_description = 'Количество лайков'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Класс для работы с изображениями в админке."""

    list_display = ('pk', 'image_link', 'post',)
    search_fields = ('post',)
