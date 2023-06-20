from datetime import datetime

import pytest
from rest_framework.test import APIClient
from users.models import CustomUser


@pytest.fixture
def client():
    return APIClient()


# фикстура для создания пользователя (не авторизованного)
@pytest.fixture
def new_user_factory():
    def create_user(
            email: str,
            password: str,
            first_name: str = None,
            last_name: str = None,
            middle_name: str = None,
            job_title: str = None,
            personal_email: str = None,
            corporate_phone_number: str = None,
            personal_phone_number: str = None,
            birthday_date: datetime = None,
            bio: str = None,
            photo: str = None,
            is_staff: bool = False,
            is_active: bool = True,
    ):
        user = CustomUser.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            job_title=job_title,
            personal_email=personal_email,
            corporate_phone_number=corporate_phone_number,
            personal_phone_number=personal_phone_number,
            birthday_date=birthday_date,
            bio=bio,
            photo=photo,
            is_staff=is_staff,
            is_active=is_active,
        )
        user.set_password(password)
        user.save()
        return user
    return create_user


# фикстура для создания авторизованного пользователя
@pytest.fixture
def authenticated_user_factory(new_user_factory, client):
    def create_user(
        email: str,
        password: str,
        first_name: str = None,
        last_name: str = None,
        middle_name: str = None,
        job_title: str = None,
        personal_email: str = None,
        corporate_phone_number: str = None,
        personal_phone_number: str = None,
        birthday_date: datetime = None,
        bio: str = None,
        photo: str = None,
        is_staff: bool = False,
        is_active: bool = True,

    ):
        user = new_user_factory(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            job_title=job_title,
            personal_email=personal_email,
            corporate_phone_number=corporate_phone_number,
            personal_phone_number=personal_phone_number,
            birthday_date=birthday_date,
            bio=bio,
            photo=photo,
            is_staff=is_staff,
            is_active=is_active,
        )
        client.post(
            '/api/v1/auth/token/login/',
            {'password': password, 'email': user.email}
        )
        return user
    return create_user
