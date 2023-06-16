import pytest

from rest_framework import status

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


class TestAddressbookEndpoints:
    path = '/api/v1/addressbook'

    def test_addressbook_get(self):
        pass


class TestUsersEndpoints:
    path = '/api/v1/users/'

    def test_users_get(self):
        pass


class TestPostsEndpoints:
    path = 'api/v1/posts/'

    def test_posts_get(self):
        pass


class TestBirthdayListEndpoints:
    path = 'api/v1/birthday_list/'

    def test_birthday_list_get(self):
        pass
