from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import TokenProxy
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'email', 'first_name', 'last_name', 'birthday_date',
        'corporate_phone_number'
    )
    list_filter = ('email', 'first_name', 'last_name')
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
        'email', 'first_name', 'last_name', 'birthday_date',
        'corporate_phone_number'
    )
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(TokenProxy)
