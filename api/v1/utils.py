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


def del_files(post):
    """Удаление файлов, связанных с постом."""
    links = [
        BASE_DIR + MEDIA_URL + file_link[0]
        for file_link in post.files.all().values_list('file_link')
    ]
    for link in links:
        try:
            os.remove(link)
        except FileNotFoundError:
            pass
