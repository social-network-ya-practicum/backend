import logging

from django.db import models

from config.settings import AUTH_USER_MODEL
from users.models import CustomUser

logger = logging.getLogger('django.db.backends')


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

    def save(
        self, force_insert=False, force_update=False,
        using=None, update_fields=None
    ):
        is_created = False
        if self.id:
            logger.info(f'Обновление поста id#{self.id} - "{self.text[:50]}"')
        else:
            logger.info(f'Создание поста - "{self.text[:50]}"')
            is_created = True
        super().save(force_insert, force_update, using, update_fields)
        if is_created:
            logger.info(f'Создан пост id#{self.id}')


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

    def save(
        self, force_insert=False, force_update=False,
        using=None, update_fields=None
    ):
        is_created = False
        if self.id:
            logger.info(
                f'Обновление изображения id#{self.id} к посту "{self.post}"'
            )
        else:
            logger.info(f'Создание изображения к посту "{self.post}"')
            is_created = True
        super().save(force_insert, force_update, using, update_fields)
        if is_created:
            logger.info(f'Создано изображение id#{self.id}')
