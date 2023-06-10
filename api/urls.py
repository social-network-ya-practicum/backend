from django.urls import include, path
from rest_framework.routers import DefaultRouter

<<<<<<< HEAD
from .views import (
    AddressBookView, BirthdayList, ChangePasswordView, CreateUsersViewSet,
    PostViewSet, ShortInfoView, UsersViewSet,
=======
from posts.views import PostViewSet
from users.views import (
    AddressBookView, BirthdayList, ChangePasswordView,
    CreateUsersViewSet, ShortInfoView, UsersViewSet
>>>>>>> b0f4c9696103ce8b48fef283236bc4e34748f070
)


app_name = 'api'

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
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
    path(
        'users/short_info/<int:user_id>/',
        ShortInfoView.as_view({'get': 'list'}),
        name='users-short-info'
    ),
    path(
        'users/<int:user_id>/posts/',
        PostViewSet.as_view({'get': 'list'}),
        name='user-posts'
    ),
    path('birthday_list/', BirthdayList.as_view()),
    path('addressbook', AddressBookView.as_view()),
]
