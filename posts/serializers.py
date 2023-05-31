from rest_framework import serializers

from posts.fields import Base64ImageField
from posts.models import Post
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    """Сериализер для модели с Post."""
    author = UserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'text', 'author', 'pub_date',
            'update_date', 'image', 'like_count'
        )
        model = Post

    def get_like_count(self, obj_post):
        """Вычисляет количество лайков у поста."""
        return obj_post.users_like.count()
