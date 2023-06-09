from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    email = models.EmailField(_('email_address'), max_length=254, unique=True)
    password = models.CharField(_('password'), max_length=150)
    first_name = models.CharField(
        _('first_name'), max_length=150, blank=True, null=True
    )
    last_name = models.CharField(
        _('last_name'), max_length=150, blank=True, null=True
    )
    middle_name = models.CharField(
        _('middle_name'), max_length=150, blank=True, null=True
    )
    job_title = models.CharField(
        _('job_title'), max_length=150, blank=True, null=True
    )
    personal_email = models.EmailField(
        _('personal_email'), max_length=254, unique=True,
        blank=True, null=True
    )
    corporate_phone_number = PhoneNumberField(
        _('phone_number'), unique=True,
        help_text=_('Format: +99999999999'),
        blank=True, null=True
    )
    personal_phone_number = PhoneNumberField(
        _('phone_number'), unique=True,
        help_text=_('Format: +99999999999'),
        blank=True, null=True
    )
    birthday_date = models.DateField(
        _('birthday_date'), blank=True, null=True,
        help_text=_('Format: YYYY-MM-DD')
    )
    bio = models.TextField(
        _('bio'), max_length=500, blank=True, null=True,
        help_text=_('Maximum 500 characters.')
    )
    photo = models.ImageField(
        _('Users Photo'),
        upload_to='users/photo/', null=True, blank=True
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
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
