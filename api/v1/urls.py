from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AddressBookView, BirthdayList, ChangePasswordView,
                    CommentsViewSet, CreateUsersViewSet, GroupViewSet,
                    PostViewSet, ShortInfoView, TokenCreateView,
                    UserPostsViewSet, UsersViewSet, СhangedTokenDestroyView)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'posts', PostViewSet, basename='posts')
router_v1.register(r'users', UsersViewSet, basename='users')
router_v1.register(r'groups', GroupViewSet, basename='groups')
router_v1.register(
    r'posts/(?P<posts_id>\d+)/comments', CommentsViewSet, basename='comments'
)

urlpatterns = [
    path('auth/token/login/', TokenCreateView.as_view()),
    path('auth/token/logout/', СhangedTokenDestroyView.as_view()),
    path(
        'users/registration/',
        CreateUsersViewSet.as_view({'post': 'create'}),
        name='registration'
    ),
    path(
        'users/<int:user_id>/posts/',
        UserPostsViewSet.as_view({'get': 'list'}),
        name='user_posts'
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
    path('birthday_list/', BirthdayList.as_view()),
    path('addressbook', AddressBookView.as_view()),
    path('', include(router_v1.urls)),
]
