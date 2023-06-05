import os

from config.settings import BASE_DIR, MEDIA_URL


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
