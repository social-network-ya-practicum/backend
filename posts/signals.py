import logging

from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import File, Post, Image

logger = logging.getLogger('django.db.backends')


@receiver(post_delete, sender=Post)
def delete_post_log_handler(sender, instance, *args, **kwargs):
    logger.info(f'Удаление поста id#{instance.id} - "{instance.text[:50]}"')


@receiver(post_delete, sender=Image)
def delete_image_log_handler(sender, instance, *args, **kwargs):
    logger.info(
        f'Удаление изображения id#{instance.id} к посту "{instance.post}"'
    )


@receiver(post_delete, sender=File)
def delete_file_log_handler(sender, instance, *args, **kwargs):
    logger.info(
        f'Удаление файла id#{instance.id} к посту "{instance.post}"'
    )
