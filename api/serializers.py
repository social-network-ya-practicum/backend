from datetime import date, datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from drf_extra_fields.fields import HybridImageField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.utils import del_images
from posts.models import Image, Post

CustomUser = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    """Сериализация изображений."""

    image_link = serializers.SerializerMethodField()

    class Meta:
        fields = ('image_link',)
        model = Image

    def get_image_link(self, obj):
        if obj.image_link:
            return f'https://csn.sytes.net/media/{str(obj.image_link)}'


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for users endpoint.
    """
    email = serializers.CharField(read_only=True)
    photo = serializers.SerializerMethodField()
    birthday_day = serializers.SerializerMethodField()
    birthday_month = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'first_name', 'last_name', 'middle_name',
            'job_title', 'personal_email', 'corporate_phone_number',
            'personal_phone_number', 'birthday_day', 'birthday_month',
            'bio', 'photo'
        )

    def get_photo(self, obj):
        if obj.photo:
            return f'https://csn.sytes.net/media/{str(obj.photo)}'

    def get_birthday_day(self, obj):
        if obj.birthday_date:
            return obj.birthday_date.day

    def get_birthday_month(self, obj):
        if obj.birthday_date:
            return obj.birthday_date.month


class PostSerializer(serializers.ModelSerializer):
    """Сериализация модели Post."""

    author = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, required=False)

    class Meta:
        fields = (
            'id', 'text', 'author', 'pub_date', 'update_date',
            'images', 'like_count', 'users_like',
        )
        model = Post

    def get_like_count(self, obj_post):
        """Вычисляет количество лайков у поста."""
        return obj_post.users_like.count()

    @staticmethod
    def create_images(post, images):
        """Сохраняет картинки к посту."""
        objs_image = (
            Image(
                post=post,
                image_link=image.get('image_link')
            ) for image in images if image
        )
        Image.objects.bulk_create(objs_image)

    @transaction.atomic
    def create(self, validate_data):
        if 'images' in validate_data:
            images = validate_data.pop('images')
            post = Post(**validate_data)
            post.save()
            self.create_images(post, images)
            return post

        return super().create(validate_data)

    @transaction.atomic()
    def update(self, instance, validate_data):
        if 'images' in validate_data:
            images = validate_data.pop('images')
            super().update(instance, validate_data)
            del_images(instance)
            Image.objects.filter(post=instance).delete()
            self.create_images(instance, images)
            return instance

        return super().update(instance, validate_data)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    model = CustomUser
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)


class ShortInfoSerializer(UserSerializer):
    """Serializer for show short info about user."""
    posts_count = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ('first_name', 'middle_name', 'job_title', 'posts_count')


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for user update.
    """
    email = serializers.CharField(read_only=True)
    photo = HybridImageField(required=False, allow_null=True)
    birthday_day = serializers.IntegerField(allow_null=True)
    birthday_month = serializers.IntegerField(allow_null=True)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'first_name', 'last_name', 'middle_name',
            'job_title', 'personal_email', 'corporate_phone_number',
            'personal_phone_number', 'birthday_day', 'birthday_month',
            'bio', 'photo'
        )

    def validate(self, data):
        day = data.get('birthday_day')
        month = data.get('birthday_month')
        if not day:
            day = 1
        if not month:
            month = 1

        try:
            bithday_date = date(year=2000, month=month, day=day)
        except ValueError:
            raise serializers.ValidationError(
                {'message': 'Неверная дата рождения'}
            )

        data['birthday_date'] = bithday_date
        return data


class CreateCustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for POST method users endpoint.
    """
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all())
        ]
    )

    class Meta:
        model = CustomUser
        fields = (
            'email', 'password'
        )
        extra_kwargs = {
            'email': {'required': True},
            'password': {
                'required': True, 'write_only': True, 'min_length': 8
            },
        }

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


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
        representation['birthday_date'] = new_format.strftime('%d %B')
        return representation


class AddressBookSerializer(serializers.ModelSerializer):
    """
    Serializer for addressbook.
    """
    email = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'first_name', 'middle_name', 'last_name',
            'job_title', 'corporate_phone_number', 'photo'
        )
