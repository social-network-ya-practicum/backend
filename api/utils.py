import os

from config.settings import BASE_DIR, MEDIA_URL
from rest_framework.views import exception_handler


def del_images(post):
    """Удаление изображений, связанных с постом."""
    links = [
        BASE_DIR + MEDIA_URL + image_link[0]
        for image_link in post.images.all().values_list('image_link')
    ]
    for link in links:
        try:
            os.remove(link)
        except FileNotFoundError:
            pass


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    try:
        response.data = {'error': response.data.get('detail', exc.detail)}
    except Exception:
        response.data = {'error': 'Запрошенный ресурс не найден.'}
    finally:
        return response
