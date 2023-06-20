import pytest

from posts.models import Post


@pytest.fixture
def post_1(authenticated_user):
    return Post.objects.create(
        text='Первый пост',
        author=authenticated_user
    )


@pytest.fixture
def post_liked(authenticated_user):
    post_liked = Post.objects.create(
        text='Первый пост',
        author=authenticated_user,
    )
    post_liked.users_like.set([authenticated_user])
    return post_liked
