from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (BirthdayList, ChangePasswordView, CreateUsersViewSet,
                    UsersViewSet)

app_name = 'users'

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')


urlpatterns = [
    path(
        'users/registration/',
        CreateUsersViewSet.as_view({'post': 'create'}),
        name='registration'
    ),
    path(
        'users/set_password/',
        ChangePasswordView.as_view(),
        name='change-password'
    ),
    path('birthday_list/', BirthdayList.as_view()),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
