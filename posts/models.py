from django.db import models

from config.settings import AUTH_USER_MODEL
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

    users_like = models.ManyToManyField(
        AUTH_USER_MODEL,
        related_name='posts_liked',
        blank=True
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:30]


class Image(models.Model):
    """Модель для изображений к посту."""

    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        related_name='images',
        on_delete=models.CASCADE,
    )
    image_link = models.ImageField(
        verbose_name='Изображение',
        upload_to='posts/images/%Y/%m/%d',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ('-post', 'id',)
