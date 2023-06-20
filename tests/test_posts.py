from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class TestPostsAPI:
    post_url = '/api/v1/posts/'
    post_detail_url = '/api/v1/posts/{id}/'
    post_like_url = '/api/v1/posts/{id}/like/'

    def test_post_list_not_found(self, client):
        response = client.get(self.post_url)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпойнт {self.post_url} не найден.'
        )

    def test_post_not_found(self, client, post_1):
        response = client.get(self.post_detail_url.format(id=post_1.id))

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпойнт {self.post_detail_url.format(id=post_1.id)} не найден.'
        )

    def test_post_like_not_found(self, client, post_1):
        response = client.get(self.post_like_url.format(id=post_1.id))

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпойнт {self.post_like_url.format(id=post_1.id)} не найден.'
        )

    def test_post_list_not_auth(self, client):
        response = client.get(self.post_url)

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'GET-запрос неавторизованного пользователя к '
            f'{self.post_url} должен возвращать ответ со статусом 401.'
        )

    def test_post_list_auth(self, user_client):
        response = user_client.get(self.post_url)

        assert response.status_code == HTTPStatus.OK, (
            'GET-запрос авторизованного пользователя к '
            f'{self.post_url} должен возвращать ответ со статусом 200.'
        )

        data = response.json()
        assert isinstance(data, list), (
            'GET-запрос авторизованного пользователя к '
            f'{self.post_url} должен возвращать список.'
        )

    def test_post_not_auth(self, client, post_1):
        response = client.get(self.post_detail_url.format(id=post_1.id))

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'GET-запрос неавторизованного пользователя к '
            f'{self.post_detail_url.format(id=post_1.id)} '
            'должен возвращать ответ со статусом 401.'
        )

    def test_post_auth(self, user_client, post_1):
        response = user_client.get(self.post_detail_url.format(id=post_1.id))

        assert response.status_code == HTTPStatus.OK, (
            'GET-запрос авторизованного пользователя к '
            f'{self.post_detail_url.format(id=post_1.id)} '
            'должен возвращать ответ со статусом 200.'
        )

    def test_post_like_not_auth(self, client, post_1):
        response = client.post(self.post_like_url.format(id=post_1.id))

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'POST-запрос неавторизованного пользователя к '
            f'{self.post_like_url.format(id=post_1.id)} '
            'должен возвращать ответ со статусом 401.'
        )

    def test_post_like_auth(self, user_client, post_1):
        response = user_client.post(self.post_like_url.format(id=post_1.id))

        assert response.status_code == HTTPStatus.CREATED, (
            'POST-запрос авторизованного пользователя к '
            f'{self.post_like_url.format(id=post_1.id)} '
            'должен возвращать ответ со статусом 201.'
        )

    def test_post_delete_like_not_auth(self, client, post_1):
        response = client.delete(self.post_like_url.format(id=post_1.id))

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'DELETE-запрос неавторизованного пользователя к '
            f'{self.post_like_url.format(id=post_1.id)} '
            'должен возвращать ответ со статусом 401.'
        )

    def test_post_delete_like_auth(self, user_client, post_liked):
        response = user_client.delete(
            self.post_like_url.format(id=post_liked.id))

        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'DELETE-запрос авторизованного пользователя к '
            f'{self.post_like_url.format(id=post_liked.id)} '
            'должен возвращать ответ со статусом 204.'
        )
