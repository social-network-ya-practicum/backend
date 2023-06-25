import logging

from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import CustomUser

logger = logging.getLogger('django.db.backends')


@receiver(post_delete, sender=CustomUser)
def delete_log_handler(sender, instance, *args, **kwargs):
    logger.info(f'Удаление пользователя - "{instance.email}"')
