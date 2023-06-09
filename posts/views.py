from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from posts.models import Post
from posts.permissions import IsAuthorAdminOrReadOnly
from posts.serializers import PostSerializer
from posts.utils import del_images


class PostViewSet(viewsets.ModelViewSet):
    """Добавление, изменение и удаление постов. Получение списка постов."""

    serializer_class = PostSerializer
    permission_classes = (IsAuthorAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if self.kwargs.get("user_id"):
            author = self.request.user
            return Post.objects.filter(author=author)
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        del_images(instance)
        super().perform_destroy(instance)

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

        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
