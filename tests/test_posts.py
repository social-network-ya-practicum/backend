from http import HTTPStatus

import pytest

from posts.models import Post


@pytest.mark.django_db(transaction=True)
class TestPostsAPI:
    post_url = '/api/v1/posts/'
    post_detail_url = '/api/v1/posts/{id}/'
    post_like_url = '/api/v1/posts/{id}/like/'

    def check_post_data(self, response_data, url):

        response_post_fields = (
            'id', 'text', 'author', 'pub_date',
            'update_date', 'images', 'like_count',
        )
        for field in response_post_fields:
            assert field in response_data, (
                f'В ответе на {url} отсутствует поле {field}.'
            )

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

    def test_post_list_auth(self, user_client, post_1):
        response = user_client.get(self.post_url)

        assert response.status_code == HTTPStatus.OK, (
            'GET-запрос авторизованного пользователя к '
            f'{self.post_url} должен возвращать ответ со статусом 200.'
        )

        data = response.json().get('results')
        assert isinstance(data, list), (
            'GET-запрос авторизованного пользователя к '
            f'{self.post_url} должен возвращать список.'
        )

        assert len(data) == Post.objects.count(), (
            'GET-запрос авторизованного пользователя к '
            f'{self.post_url} вернул не все посты.'
        )

        self.check_post_data(data[0], self.post_url)

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
        test_post = Post.objects.get(id=post_1.id)
        count_like = test_post.users_like.count()
        response = client.post(self.post_like_url.format(id=post_1.id))

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'POST-запрос неавторизованного пользователя к '
            f'{self.post_like_url.format(id=post_1.id)} '
            'должен возвращать ответ со статусом 401.'
        )

        assert count_like == test_post.users_like.count(), (
            'POST-запрос неавторизованного пользователя к '
            f'{self.post_like_url.format(id=post_1.id)} '
            'не должен изменять количество лайков'
        )

    def test_post_like_auth(self, user_client, post_1):
        test_post = Post.objects.get(id=post_1.id)
        count_like = test_post.users_like.count()
        response = user_client.post(self.post_like_url.format(id=post_1.id))

        assert response.status_code == HTTPStatus.CREATED, (
            'POST-запрос авторизованного пользователя к '
            f'{self.post_like_url.format(id=post_1.id)} '
            'должен возвращать ответ со статусом 201.'
        )

        count_like += 1
        assert count_like == test_post.users_like.count(), {
            'POST-запрос авторизованного пользователя к '
            f'{self.post_like_url.format(id=post_1.id)} '
            'должен увеличить количество лайков.'
        }

    def test_post_delete_like_not_auth(self, client, post_liked):
        test_post = Post.objects.get(id=post_liked.id)
        count_like = test_post.users_like.count()
        response = client.delete(self.post_like_url.format(id=post_liked.id))

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'DELETE-запрос неавторизованного пользователя к '
            f'{self.post_like_url.format(id=post_liked.id)} '
            'должен возвращать ответ со статусом 401.'
        )

        assert count_like == test_post.users_like.count(), {
            'DELETE-запрос неавторизованного пользователя к '
            f'{self.post_like_url.format(id=post_liked.id)} '
            'должен изменять количество лайков.'
        }

    def test_post_delete_like_auth(self, user_client, post_liked):
        test_post = Post.objects.get(id=post_liked.id)
        count_like = test_post.users_like.count()
        response = user_client.delete(
            self.post_like_url.format(id=post_liked.id))

        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'DELETE-запрос авторизованного пользователя к '
            f'{self.post_like_url.format(id=post_liked.id)} '
            'должен возвращать ответ со статусом 204.'
        )

        count_like -= 1
        assert count_like == test_post.users_like.count(), {
            'DELETE-запрос авторизованного пользователя к '
            f'{self.post_like_url.format(id=post_liked.id)} '
            'должен уменьшать количество лайков.'
        }

    def test_post_create_auth_with_invalid_data(self, user_client):
        post_count = Post.objects.count()
        response = user_client.post(self.post_url, data={})

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Для авторизованного пользователя POST-запрос с '
            f'некорректными данными к {self.post_url} '
            'должен вернуть ответ со статусом 400.'
        )

        assert post_count == Post.objects.count(), (
            'Для авторизованного пользователя POST-запрос с '
            f'некорректными данными к {self.post_url} '
            'не должен изменить количество постов.'
        )

    def test_post_create_auth_with_valid_data(self, user_client):
        post_count = Post.objects.count()
        data = {'text': 'Пост'}
        response = user_client.post(self.post_url, data=data)

        assert response.status_code == HTTPStatus.CREATED, (
            'Для авторизованного пользователя POST-запрос с '
            f'корректными данными к {self.post_url} '
            'должен вернуть ответ со статусом 201.'
        )

        post_count += 1

        assert post_count == Post.objects.count(), (
            'Для авторизованного пользователя POST-запрос с '
            f'корректными данными к {self.post_url} '
            'создает новый пост.'
        )

        data_post = response.json()

        assert isinstance(data_post, dict), (
            'POST-запрос авторизованного пользователя к '
            f'{self.post_url} не вернул ответ в виде словаря.'
        )

        self.check_post_data(data_post, self.post_url)

    def test_post_unauth_create(self, client):
        post_count = Post.objects.count()
        data = {'text': 'Пост'}
        response = client.post(self.post_url, data=data)

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'POST-запрос неавторизованного пользователя к '
            f'{self.post_url} должен вернуть ответ со статусом 401.'
        )

        assert post_count == Post.objects.count(), (
            'POST-запрос неавторизованного пользователя к '
            f'{self.post_url} не должен создавать новый пост.'
        )

    def test_post_detail_auth(self, user_client, post_1):
        response = user_client.get(self.post_detail_url.format(id=post_1.id))

        assert response.status_code == HTTPStatus.OK, (
            'GET-запрос авторизованного пользователя к '
            f'{self.post_detail_url} должен вернуть ответ со статусом 200.'
        )

        data = response.json()
        self.check_post_data(data, f'GET-запрос к {self.post_detail_url}')

    def test_post_put_unauth_with_valid_data(self, client, post_1):
        data = {'text': 'Обновленный пост'}

        response = client.put(
            self.post_detail_url.format(id=post_1.id),
            data=data
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'PUT-запрос неавторизованного пользователя к '
            f'{self.post_detail_url.format(id=post_1.id)} '
            'должен вернуть ответ со статусом 401.'
        )

        post_test = Post.objects.filter(id=post_1.id).first()
        assert post_test.text != data.get('text'), (
            'PUT-запрос неавторизованного пользователя к '
            f'{self.post_detail_url.format(id=post_1.id)}'
            'не должен изменить пост.'
        )

    def test_post_put_auth_with_valid_data(self, user_client, post_1):
        data = {'text': 'Обновленный пост'}

        response = user_client.put(
            self.post_detail_url.format(id=post_1.id),
            data=data
        )
        assert response.status_code == HTTPStatus.OK, (
            'PUT-запрос авторизованного пользователя к '
            f'{self.post_detail_url.format(id=post_1.id)} '
            'должен вернуть ответ со статусом 200.'
        )

        post_test = Post.objects.filter(id=post_1.id).first()
        assert post_test.text == data.get('text'), (
            'PUT-запрос авторизованного пользователя к '
            f'{self.post_detail_url.format(id=post_1.id)}'
            'должен изменить пост.'
        )

        data = response.json()
        self.check_post_data(data, f'PUT-запрос к {self.post_detail_url}')

    def test_post_delete_auth(self, user_client, post_1):
        response = user_client.delete(self.post_detail_url.format(id=post_1.id))

        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'DELETE-запрос авторизованного пользователя к '
            f'{self.post_detail_url} должен вернуть ответ со статусом 204.'
        )

    def test_post_delete_unauth(self, client, post_1):
        response = client.delete(self.post_detail_url.format(id=post_1.id))

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'DELETE-запрос неавторизованного пользователя к '
            f'{self.post_detail_url} должен вернуть ответ со статусом 401.'
        )

        post_test = Post.objects.filter(id=post_1.id).first()

        assert post_test, (
            'DELETE-запрос неавторизованного пользователя к '
            f'{self.post_detail_url} не должен удалять пост.'
        )