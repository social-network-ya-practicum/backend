from django.urls import include, path
from rest_framework import routers

from posts.views import PostViewSet
from users.views import BirthdayList


app_name = 'api'
router_v1 = routers.DefaultRouter()

router_v1.register(r'posts', PostViewSet, basename='posts')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('birthday_list/', BirthdayList.as_view())
]
