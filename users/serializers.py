from rest_framework import serializers

from users.models import CustomUser


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

    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name', 'last_name', 'password', 'phone_number',
            'birthday_date'
        )


class CreateCustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for POST method users endpoint.
    """

    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name', 'last_name', 'password', 'phone_number',
            'birthday_date'
        )
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True, 'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True},
            'birthday_date': {'required': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            birthday_date=validated_data['birthday_date'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
