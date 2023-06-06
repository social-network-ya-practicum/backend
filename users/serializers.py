from datetime import date, datetime

from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

CustomUser = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    model = CustomUser
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for users endpoint.
    """

    photo = Base64ImageField(required=False, allow_null=True)
    birthday_day = serializers.SerializerMethodField()
    birthday_month = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name', 'last_name', 'middle_name', 'job_title',
            'personal_email', 'corporate_phone_number',
            'personal_phone_number', 'birthday_day', 'birthday_month',
            'bio', 'photo'
        )

    def get_birthday_day(self, obj):
        if obj.birthday_date:
            return obj.birthday_date.day

    def get_birthday_month(self, obj):
        if obj.birthday_date:
            return obj.birthday_date.month


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for user update.
    """

    photo = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'middle_name', 'job_title',
            'personal_email', 'corporate_phone_number',
            'personal_phone_number', 'birthday_date',
            'bio', 'photo'
        )

    def validate_birthday_date(self, value):
        today = date.today()
        if value > today:
            raise serializers.ValidationError(
                'Birthday cannot be in the future.'
            )
        if 1929 < value.year > 2011:
            raise serializers.ValidationError('You are so young or so old.')
        return value


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

    class Meta:
        model = CustomUser
        fields = (
            'id', 'first_name', 'middle_name', 'last_name', 'job_title',
            'email', 'corporate_phone_number', 'photo'
        )
