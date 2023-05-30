from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField, HybridImageField
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

    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name', 'last_name', 'phone_number',
            'birthday_date', 'middle_name', 'bio', 'photo'
        )


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
    photo = HybridImageField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name', 'last_name', 'password', 'phone_number',
            'birthday_date', 'middle_name', 'bio', 'photo'
        )
        extra_kwargs = {
            'email': {'required': True},
            'password': {
                'required': True, 'write_only': True, 'min_length': 8
            },
            'first_name': {'required': True},
            'last_name': {'required': True},
            'middle_name': {'required': True},
            'phone_number': {'required': True},
            'birthday_date': {'required': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data['middle_name'],
            phone_number=validated_data['phone_number'],
            birthday_date=validated_data['birthday_date'],
            bio=validated_data['bio'],
            photo=validated_data['photo']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
