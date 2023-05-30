from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .mixins import CreateUpdateListRetrieveViewSet
from .models import CustomUser
from .serializers import (ChangePasswordSerializer, CreateCustomUserSerializer,
                          UserSerializer)


class ChangePasswordView(CreateAPIView):
    """Change password view."""

    serializer_class = ChangePasswordSerializer
    model = CustomUser

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(
                serializer.validated_data.get('current_password')
            ):
                return Response(
                    {_('current_password'): _('Wrong password.')},
                    status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(
                serializer.validated_data.get('new_password'))
            self.object.save()
            return Response(
                {_('message'): _('Password updated successfully')},
                status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(CreateUpdateListRetrieveViewSet):
    """Users view."""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserSerializer
        return CreateCustomUserSerializer

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        user_instance = self.request.user
        serializer = self.get_serializer(user_instance)
        return Response(serializer.data, status.HTTP_200_OK)
