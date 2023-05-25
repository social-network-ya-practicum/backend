from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'email', 'first_name', 'last_name', 'password', 'phone_number',
        'birthday_date'
    )
    list_filter = ('email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'password1', 'password2',
                'phone_number', 'birthday_date', 'is_staff', 'is_active')}),
    )
    search_fields = (
        'email', 'first_name', 'last_name', 'birthday_date', 'phone_number'
    )
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
