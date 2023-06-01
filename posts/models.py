from django.db import models

from config import settings
from users.models import CustomUser


class Post(models.Model):
    """Модель поста."""

    text = models.TextField(
        verbose_name='Текст',
        max_length=40000,
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    update_date = models.DateTimeField(
        verbose_name='Последнее обновление',
        auto_now=True,
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='posts/images/',
        null=True,
        blank=True,
    )
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='posts_liked',
        blank=True
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:30]
