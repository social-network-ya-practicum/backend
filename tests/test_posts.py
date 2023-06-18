from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class TestPostsAPI:
    post_url = '/api/v1/posts/'
    post_detail_url = '/api/v1/posts/{id}/'

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


