from datetime import date, datetime

import filetype
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from drf_extra_fields.fields import (Base64FileField, Base64ImageField,
                                     HybridImageField)
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from api.v1.utils import del_files, del_images
from posts.models import Comment, File, Group, Image, Post

CustomUser = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    """Сериализация изображений."""

    image_link = Base64ImageField(required=False)

    class Meta:
        fields = ('image_link',)
        model = Image

    # def get_image_link(self, obj):
    #     if obj.image_link:
    #         return f'https://csn.sytes.net/media/{str(obj.image_link)}'


class IdPhotoUserSerializer(serializers.ModelSerializer):
    """Short representation of User for groups serialization."""

    class Meta:
        model = CustomUser
        fields = ('id', 'photo')


class FileField(Base64FileField):
    ALLOWED_TYPES = [
        'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt',
        'pdf', 'rtf', 'zip', 'rar',
        'png', 'jgp', 'webp', 'gif', 'tif', 'bmp',
        'mp3', 'wav', 'mp4', 'mkv', 'webm', 'mov', 'avi', 'mpg'
    ]

    def get_file_extension(self, filename, decoded_file):
        file_type = filetype.guess(decoded_file)
        return file_type.extension


class FileSerializer(serializers.ModelSerializer):
    """Сериализация файлов."""

    file_link = FileField(required=False)

    class Meta:
        fields = ('file_link', 'file_title')
        model = File

    def get_file_link(self, obj):
        if obj.file_link:
            return f'https://csn.sytes.net/media/{str(obj.file_link)}'


class UserShortInfoSerializer(serializers.ModelSerializer):
    """Короткая информация о пользователе в постах"""
    class Meta:
        model = CustomUser
        fields = (
            'id', 'first_name', 'last_name', 'photo', 'is_staff'
        )


class PostSerializer(serializers.ModelSerializer):
    """Сериализация модели Post."""

    author = UserShortInfoSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, required=False)
    files = FileSerializer(many=True, required=False)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False
    )
    comments = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'text', 'author', 'pub_date', 'update_date',
            'images', 'files', 'like_count', 'likes', 'group', 'comments'
        )
        model = Post

    def get_like_count(self, obj_post):
        """Вычисляет количество лайков у поста."""
        return obj_post.likes.count()

    def get_comments(self, obj):
        queryset = Comment.objects.filter(post=obj)
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data

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

    @staticmethod
    def create_files(post, files):
        """Сохраняет файлы к посту."""
        objs_file = (
            File(
                post=post,
                file_link=file.get('file_link'),
                file_title=file.get('file_title'),
            ) for file in files if file
        )
        File.objects.bulk_create(objs_file)

    @transaction.atomic
    def create(self, validate_data):
        attrib = {
            'images': None,
            'files': None
        }
        is_image_file = False
        for key in attrib:
            if key in validate_data:
                attrib[key] = validate_data.pop(key)
                is_image_file = True
        if is_image_file:
            post = Post(**validate_data)
            post.save()
            if attrib['images']:
                self.create_images(post, attrib['images'])
            if attrib['files']:
                if len(attrib['files']) > 10:
                    raise serializers.ValidationError(
                        'Возможно добавление не более 10 файлов.'
                    )
                self.create_files(post, attrib['files'])
            return post
        return super().create(validate_data)

    @transaction.atomic()
    def update(self, instance, validate_data):
        attrib = {
            'images': None,
            'files': None
        }
        is_image_file = False
        for key in attrib:
            if key in validate_data:
                attrib[key] = validate_data.pop(key)
                is_image_file = True
        if is_image_file:
            super().update(instance, validate_data)
            if attrib['images']:
                del_images(instance)
                Image.objects.filter(post=instance).delete()
                self.create_images(instance, attrib['images'])
            if attrib['files']:
                if len(attrib['files']) > 10:
                    raise serializers.ValidationError(
                        'Возможно добавление не более 10 файлов.'
                    )
                del_files(instance)
                File.objects.filter(post=instance).delete()
                self.create_files(instance, attrib['files'])
            return instance
        return super().update(instance, validate_data)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for users endpoint.
    """
    email = serializers.CharField(read_only=True)
    photo = Base64ImageField(required=False)
    birthday_day = serializers.SerializerMethodField()
    birthday_month = serializers.SerializerMethodField()
    posts = PostSerializer(many=True)
    followings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'first_name', 'last_name', 'middle_name',
            'job_title', 'personal_email', 'corporate_phone_number',
            'personal_phone_number', 'birthday_day', 'birthday_month',
            'bio', 'photo', 'department', 'posts', 'followings'
        )

    # def get_photo(self, obj):
    #     if obj.photo:
    #         return f'https://csn.sytes.net/media/{str(obj.photo)}'

    def get_birthday_day(self, obj):
        if obj.birthday_date:
            return obj.birthday_date.day

    def get_birthday_month(self, obj):
        if obj.birthday_date:
            return obj.birthday_date.month


class CommentSerializer(serializers.ModelSerializer):
    author = UserShortInfoSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'like_count', 'like')
        model = Comment

    def get_like_count(self, obj):
        """Вычисляет количество лайков у комментария."""
        return obj.like.count()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    model = CustomUser
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)


class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = SlugRelatedField(slug_field='id', read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    followers_count = serializers.ReadOnlyField(source='followers.count')
    created_date = serializers.DateTimeField()
    image_link = Base64ImageField(required=False)
    followers = IdPhotoUserSerializer(many=True)
    resume = serializers.CharField(read_only=True)
    posts_group = PostSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = (
            'title', 'description', 'created_date',
            'author', 'image_link', 'followers_count',
            'followers', 'posts_group', 'resume'
        )


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
            'bio', 'photo', 'department',
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


class ResponseCreateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email',)


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
        try:
            validate_password(password=validated_data['password'], user=user)
        except ValidationError as err:
            raise serializers.ValidationError({'password': err.messages})
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
            'job_title', 'corporate_phone_number', 'photo', 'department'
        )
