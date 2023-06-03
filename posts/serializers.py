from datetime import datetime

from rest_framework import serializers

from posts.fields import Base64ImageField
from posts.models import Post
from users.models import CustomUser
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


class BirthdaySerializer(serializers.ModelSerializer):
    """Сериализер для дней рождений"""
    birthday_date = serializers.DateField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'photo',
            'first_name',
            'last_name',
            'birthday_date',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        birthday_date = representation.get('birthday_date')
        new_format = datetime.strptime(birthday_date, '%Y-%m-%d').date()
        representation['birthday_date'] = new_format.strftime('%-d %B')
        return representation
