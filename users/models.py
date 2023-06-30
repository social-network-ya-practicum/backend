import logging

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from api.managers import CustomUserManager

logger = logging.getLogger('django.db.backends')


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    email = models.EmailField(
        _('Корпоративная почта'), max_length=254, unique=True
    )
    password = models.CharField(_('Пароль'), max_length=150)
    first_name = models.CharField(
        _('Имя'), max_length=150, blank=True, null=True
    )
    last_name = models.CharField(
        _('Фамилия'), max_length=150, blank=True, null=True
    )
    middle_name = models.CharField(
        _('Отчество'), max_length=150, blank=True, null=True
    )
    job_title = models.CharField(
        _('Должность'), max_length=150, blank=True, null=True
    )
    personal_email = models.EmailField(
        _('Личная почта'), max_length=254, unique=True,
        blank=True, null=True
    )
    corporate_phone_number = PhoneNumberField(
        _('Корпоративный номер телефона'), unique=True,
        help_text=_('Формат: +99999999999'),
        blank=True, null=True
    )
    personal_phone_number = PhoneNumberField(
        _('Личный номер телефона'), unique=True,
        help_text=_('Формат: +99999999999'),
        blank=True, null=True
    )
    birthday_date = models.DateField(
        _('День рождения'), blank=True, null=True,
        help_text=_('Формат: ГГГГ-ММ-ДД/ДД.ММ.ГГГГ')
    )
    bio = models.TextField(
        _('Биография'), max_length=500, blank=True, null=True,
        help_text=_('Максимум 500 знаков.')
    )
    photo = models.ImageField(
        _('Фотография'),
        upload_to='users/photo/', null=True, blank=True
    )

    date_joined = models.DateTimeField(
        _('Дата создания аккаунта'), default=timezone.now
    )
    is_staff = models.BooleanField(
        _('Статус администратора'),
        default=False,
        help_text=_(
            'Определяет, может ли пользователь войти на этот сайт '
            'с правами администратора.'
        ),
    )
    is_active = models.BooleanField(
        _('Статус активности'),
        default=True,
        help_text=_(
            'Указывает возможность пользователя войти на портал. '
            'Снимите чекбокс вместо удаления учетной записи.'
        ),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'password'
    ]

    class Meta:
        ordering = ('-date_joined',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def save(
        self, force_insert=False, force_update=False,
        using=None, update_fields=None
    ):
        if self.id:
            logger.info(f'Обновление пользователя - "{self.email}"')
        else:
            logger.info(f'Создание пользователя - "{self.email}"')
        super().save(force_insert, force_update, using, update_fields)
