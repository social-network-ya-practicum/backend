from django.contrib import admin
from django.db.models import Count

from config.settings import PAGINATION_LIMIT_IN_ADMIN_PANEL
from posts.models import Image, Post, Comment, Group

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


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Класс для работы с постами в админ-панели."""

    list_display = (
        'pk', 'title', 'author', 'description', 'created_date',
        'get_followers_count', 'get_posts_count', 'get_comments_count',
        'get_posts_likes_count', 'get_comments_likes_count',
    )
    list_display_links = ('title',)
    search_fields = ('title', 'description', 'author')
    list_filter = ('created_date', 'author')
    ordering = ('-created_date',)
    empty_value_display = '-пусто-'
    list_per_page = PAGINATION_LIMIT_IN_ADMIN_PANEL

    @admin.display(description='Количество подписчиков')
    def get_followers_count(self, obj):
        return obj.followers.count()

    @admin.display(description='Количество постов')
    def get_posts_count(self, obj):
        return obj.posts_group.count()

    @admin.display(description='Количество комментов')
    def get_comments_count(self, obj):
        posts = obj.posts_group.all()
        return Comment.objects.filter(post__in=posts).count()

    @admin.display(description='Количество лайков на постах')
    def get_posts_likes_count(self, obj):
        posts_likes = obj.posts_group.aggregate(likes_count=Count('likes'))
        return posts_likes['likes_count']

    @admin.display(description='Количество лайков на комментах')
    def get_comments_likes_count(self, obj):
        comments = Comment.objects.filter(post__in=obj.posts_group.all())
        comments_likes = comments.aggregate(likes_count=Count('like'))
        return comments_likes['likes_count']


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
