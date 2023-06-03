from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import Post
#from posts.permissions import IsAuthorAdminOrReadOnly
from posts.serializers import BirthdaySerializer, PostSerializer
from users.models import CustomUser


class PostViewSet(viewsets.ModelViewSet):
    """Добавление, изменение и удаление постов. Получение списка постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = (IsAuthorAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        url_path='like',
        methods=['post', 'delete'],
        detail=True,
    )
    def get_like(self, request, pk):
        """Лайкнуть пост, отменить лайк."""
        post = get_object_or_404(Post, id=pk)
        if request.method == 'POST':
            post.users_like.add(request.user)
            return Response(
                PostSerializer(post).data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            post.users_like.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)


class BirthdayList(generics.ListAPIView):
    serializer_class = BirthdaySerializer

    def get_queryset(self):
        today = datetime.now().date()
        current_month = today.month
        current_day = today.day
        queryset = CustomUser.objects.filter(
            birthday_date__day__gte=current_day,
            birthday_date__day__lte=(current_day + 3),
            birthday_date__month=current_month,
        ).order_by('birthday_date')[:3]
        return queryset
