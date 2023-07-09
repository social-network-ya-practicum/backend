from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from config.settings import PAGINATION_LIMIT_IN_ADMIN_PANEL
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'id', 'email', 'first_name', 'last_name', 'middle_name',
        'birthday_date', 'job_title', 'get_posts_count', 'get_comments_count',
        'get_likes_count', 'corporate_phone_number', 'personal_email',
        'personal_phone_number', 'bio',
    )
    list_filter = ('date_joined', 'last_name')
    list_display_links = ('email',)
    fieldsets = (
        (None, {'fields': (
            'email', 'first_name', 'last_name',
            'middle_name', 'birthday_date', 'job_title', 'personal_email',
            'corporate_phone_number', 'personal_phone_number', 'bio',
            'photo'
        )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'first_name', 'last_name',
                'middle_name', 'birthday_date', 'job_title', 'personal_email',
                'corporate_phone_number', 'personal_phone_number', 'bio',
                'photo', 'is_staff', 'is_active')}),
    )
    search_fields = (
        'email', 'first_name', 'middle_name', 'last_name', 'birthday_date',
        'corporate_phone_number'
    )
    ordering = ('-date_joined',)
    list_per_page = PAGINATION_LIMIT_IN_ADMIN_PANEL
    empty_value_display = '-пусто-'

    @admin.display(description='Количество лайков посты+комменты')
    def get_likes_count(self, obj):
        return obj.posts_liked.count() + obj.comments_likes.count()

    @admin.display(description='Количество постов')
    def get_posts_count(self, obj):
        return obj.posts.count()

    @admin.display(description='Количество комментариев')
    def get_comments_count(self, obj):
        return obj.comments.count()


admin.site.unregister(Group)
