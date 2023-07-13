import pytest

from rest_framework import status

from users.models import CustomUser

pytestmark = pytest.mark.django_db


class TestAuthEndpoints:
    path = '/api/v1/auth/token/'

    @pytest.mark.parametrize(
        'user_email, user_password, login_email, login_password, validity',
        [
            (
                'test_user@mail.com', 'password',
                'test_user@mail.com', 'password',
                status.HTTP_200_OK
            ),
            (
                'test_user@mail.com', 'password',
                'test_user@mail.com', 'wrong_password',
                status.HTTP_400_BAD_REQUEST
            ),
            (
                'test_user@mail.com', 'password',
                'wrong@mail.com', 'password',
                status.HTTP_400_BAD_REQUEST
            ),
        ]
    )
    def test_login_user_post(
        self, new_user_factory, client,
        user_email, user_password, login_email, login_password, validity
    ):
        user = new_user_factory(email=user_email, password=user_password)
        response = client.post(
            f'{self.path}login/',
            {'password': login_password, 'email': login_email}
        )
        assert response.status_code == validity
        if response.status_code == status.HTTP_200_OK:
            assert response.data['auth_token'] == user.auth_token.key

    @pytest.mark.parametrize(
        'email, password, is_authenticated, validity',
        [
            ('test@mail.com', 'password', True, status.HTTP_204_NO_CONTENT),
            ('test@mail.com', 'password', False, status.HTTP_401_UNAUTHORIZED),
        ]
    )
    def test_logout_user_post(
        self, authenticated_user_factory, new_user_factory, client,
        email, password, is_authenticated, validity,
    ):
        user = (
            authenticated_user_factory(email=email, password=password)
            if is_authenticated
            else new_user_factory(email=email, password=password)
        )
        token = user.auth_token.key if is_authenticated else None
        response = client.post(
            f'{self.path}logout/',
            HTTP_AUTHORIZATION=f'Token {token}'
        )
        assert response.status_code == validity


class TestUsersEndpoints:
    path = '/api/v1/users'

    messages_set_password = {
        'auth_right_current_password': f'Post-запрос к {path}/set_password/ '
        'авторизованного пользователя с верным current_password '
        'должен возвращать ответ со статусом 200.',

        'auth_invalid_new_password': f'Post-запрос к {path}/set_password/ '
        'авторизованного пользователя с невалидным new_password '
        'должен возвращать ответ со статусом 400.',

        'auth_wrong_current_password': f'Post-запрос к {path}/set_password/ '
        'авторизованного пользователя с неверным current_password '
        'должен возвращать ответ со статусом 400.',

        'not_auth_right_current_password':
        f'Post-запрос к {path}/set_password/ '
        'неавторизованного пользователя '
        'должен возвращать ответ со статусом 401.',
    }

    @pytest.mark.parametrize(
        'new_password,current_password,is_authenticated,validity,message_key',
        [
            (
                'Password235', 'Password23', True, status.HTTP_200_OK,
                'auth_right_current_password'
            ),
            (
                'password235', 'Password23', True,
                status.HTTP_400_BAD_REQUEST, 'auth_invalid_new_password'
            ),
            (
                'Password235', 'Password2', True,
                status.HTTP_400_BAD_REQUEST, 'auth_wrong_current_password'
            ),
            (
                'Password235', 'Password23', False,
                status.HTTP_401_UNAUTHORIZED, 'not_auth_right_current_password'
            ),
        ]
    )
    def test_set_password_post(
        self, authenticated_user_factory, new_user_factory, client,
        new_password, current_password, is_authenticated, validity, message_key
    ):
        email, password = 'test@mail.com', 'Password23'
        user = (
            authenticated_user_factory(email=email, password=password)
            if is_authenticated
            else new_user_factory(email=email, password=password)
        )
        token = user.auth_token.key if is_authenticated else None
        response = client.post(
            f'{self.path}/set_password/',
            {
                'new_password': new_password,
                'current_password': current_password
            },
            HTTP_AUTHORIZATION=f'Token {token}'
        )
        assert response.status_code == validity, (
            self.messages_set_password[message_key]
        )

    messages_registration = {
        'valid_password': f'Post-запрос к {path}/registration/ с валидными'
        ' email и password должен возвращать ответ со статусом 201.',

        'invalid_password_special': f'Post-запрос к {path}/registration/ '
        'с валидным email и невалидным password, содержащим лишние спец.'
        'символы, должен возвращать ответ со статусом 400.',

        'invalid_password_cyrillic': f'Post-запрос к {path}/registration/ '
        'с валидным email и невалидным password, содержащим кириллицу, '
        'должен возвращать ответ со статусом 400.',

        'invalid_password_space': f'Post-запрос к {path}/registration/ '
        'с валидным email и невалидным password, содержащим пробел, '
        'должен возвращать ответ со статусом 400.',

        'invalid_password_no_latin_upper':
        f'Post-запрос к {path}/registration/ '
        'с валидным email и невалидным password, отсутствует заглавная '
        'латиница, должен возвращать ответ со статусом 400.',

        'invalid_password_no_latin_lower':
        f'Post-запрос к {path}/registration/ '
        'с валидным email и невалидным password, отсутствует строчная '
        'латиница, должен возвращать ответ со статусом 400.',

        'invalid_password_no_digit':
        f'Post-запрос к {path}/registration/ '
        'с валидным email и невалидным password, отсутствует цифра, '
        'должен возвращать ответ со статусом 400.',
    }

    @pytest.mark.parametrize(
        'email, password, validity, message_key',
        [
            (
                'test@mail.com', 'aZxkeapme88', status.HTTP_201_CREATED,
                'valid_password'
            ),
            (
                'test@mail.com', '!;;%:,.;', status.HTTP_400_BAD_REQUEST,
                'invalid_password_special'
            ),
            (
                'test@mail.com', 'aапролme88', status.HTTP_400_BAD_REQUEST,
                'invalid_password_cyrillic'
            ),
            (
                'test@mail.com', 'aZxke apme88', status.HTTP_400_BAD_REQUEST,
                'invalid_password_space'
            ),
            (
                'test@mail.com', 'axkeapme88', status.HTTP_400_BAD_REQUEST,
                'invalid_password_no_latin_upper'
            ),
            (
                'test@mail.com', 'AXKEAMPME88', status.HTTP_400_BAD_REQUEST,
                'invalid_password_no_latin_lower'
            ),
            (
                'test@mail.com', 'aZxkeYapme', status.HTTP_400_BAD_REQUEST,
                'invalid_password_no_digit'
            ),
        ]
    )
    def test_registration_user_post(
        self, client,
        email, password, validity, message_key,
    ):
        response = client.post(
            f'{self.path}/registration/',
            {'email': email, 'password': password}
        )
        assert response.status_code == validity, (
            self.messages_registration[message_key]
        )
        user = CustomUser.objects.filter(email=email)
        print(user.exists())
        if validity == status.HTTP_201_CREATED:
            assert user.exists() is True
        else:
            assert user.exists() is False
