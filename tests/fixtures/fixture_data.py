import pytest

from posts.models import Post


@pytest.fixture
def post_1(authenticated_user):
    return Post.objects.create(
        text='Первый пост',
        author=authenticated_user
    )
