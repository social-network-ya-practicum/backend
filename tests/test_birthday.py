import pytest
from rest_framework import status
import datetime as dt

pytestmark = pytest.mark.django_db


class TestBirthday:
    path = '/api/v1/birthday_list/'

    def test_birthday_list_limit(
            self, authenticated_user_factory, new_user_factory, client,
    ):
        user1 = authenticated_user_factory(
            email='user1@mail.com',
            password='password',
            birthday_date=(dt.datetime.today() + dt.timedelta(days=1))
            .strftime('%Y-%m-%d')
        )
        authenticated_user_factory(
            email='user2@mail.com',
            password='password',
            birthday_date=(dt.datetime.today() + dt.timedelta(days=2))
            .strftime('%Y-%m-%d')
        )
        authenticated_user_factory(
            email='user3@mail.com',
            password='password',
            birthday_date=(dt.datetime.today())
            .strftime('%Y-%m-%d')
        )
        authenticated_user_factory(
            email='user4@mail.com',
            password='password',
            birthday_date=(dt.datetime.today() + dt.timedelta(days=2))
            .strftime('%Y-%m-%d')
        )
        token = user1.auth_token.key
        response = client.get(
            self.path,
            HTTP_AUTHORIZATION=f"Token {token}",
        )
        test_data_list = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert len(test_data_list) <= 3

    def test_no_birthday(
        self, authenticated_user_factory, new_user_factory, client,
    ):
        user1 = authenticated_user_factory(
            email='user1@mail.com',
            password='password',
            birthday_date=(dt.datetime.today() + dt.timedelta(days=5))
            .strftime('%Y-%m-%d')
        )
        authenticated_user_factory(
            email='user2@mail.com',
            password='password',
            birthday_date=(dt.datetime.today() + dt.timedelta(days=4))
            .strftime('%Y-%m-%d')
        )
        authenticated_user_factory(
            email='user3@mail.com',
            password='password',
            birthday_date=(dt.datetime.today() + dt.timedelta(days=7))
            .strftime('%Y-%m-%d')
        )
        authenticated_user_factory(
            email='user4@mail.com',
            password='password',
            birthday_date=(dt.datetime.today() + dt.timedelta(days=6))
            .strftime('%Y-%m-%d')
        )
        token = user1.auth_token.key
        response = client.get(
            self.path,
            HTTP_AUTHORIZATION=f"Token {token}",
        )
        test_data_list = response.json()
        assert len(test_data_list) == 0
        for test_data in test_data_list:
            assert test_data.get(
                'birthday_date'
            ) == dt.datetime.strptime(
                user1.birthday_date, '%Y-%m-%d'
            ).strftime('%d %B')
