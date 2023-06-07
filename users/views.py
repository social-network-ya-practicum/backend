import calendar
from datetime import datetime

from django.db.models import IntegerField, Value
from django.utils.translation import gettext_lazy as _
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from posts.models import Post
from .filters import filter_birthday
from .mixins import CreateViewSet, UpdateListRetrieveViewSet
from .models import CustomUser
from .pagination import AddressBookSetPagination
from .permissions import IsUserOrReadOnly
from .serializers import (
    AddressBookSerializer, BirthdaySerializer, ChangePasswordSerializer,
    CreateCustomUserSerializer, ShortInfoSerializer, UserSerializer,
    UserUpdateSerializer,
)


class ChangePasswordView(CreateAPIView):
    """Change password view."""

    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

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


class UsersViewSet(UpdateListRetrieveViewSet):
    """Users view."""

    actions_list = ['PUT', 'PATCH']
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method in self.actions_list:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.request.method in self.actions_list:
            permission_classes = (IsUserOrReadOnly,)
        else:
            permission_classes = (permissions.IsAuthenticated,)
        return [permission() for permission in permission_classes]

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,))
    def me(self, request):
        user_instance = self.request.user
        serializer = self.get_serializer(user_instance)
        return Response(serializer.data, status.HTTP_200_OK)


class CreateUsersViewSet(CreateViewSet):
    """Create users view."""

    queryset = CustomUser.objects.all()
    serializer_class = CreateCustomUserSerializer
    permission_classes = (AllowAny,)


class ShortInfoView(viewsets.ReadOnlyModelViewSet):
    """Short info about user."""

    serializer_class = ShortInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return CustomUser.objects.filter(id=user_id).annotate(
            posts_count=Value(Post.objects.filter(author_id=user_id).count(),
                              output_field=IntegerField())
        )


class BirthdayList(ListAPIView):
    """Сериалайзер для дней рождения"""
    serializer_class = BirthdaySerializer

    def get_queryset(self):
        today = datetime.now().date()
        current_day = today.day
        current_month = today.month
        current_year = today.year
        next_month = today.month + 1
        day_one = 30
        day_two = 31
        amount_day = calendar.monthrange(current_year, current_month)[1]
        """Если февраль високосный год"""
        if current_month == 2 and amount_day == 29:
            return filter_birthday(current_day,
                                   current_month,
                                   next_month,
                                   day_one - 2,
                                   day_two - 2)
        """Если февраль невисокосный год"""
        if current_month == 2 and amount_day == 28:
            return filter_birthday(current_day,
                                   current_month,
                                   next_month,
                                   day_one - 3,
                                   day_two - 3)
        """Нечетный месяц"""
        if current_month % 2 != 0:
            return filter_birthday(current_day,
                                   current_month,
                                   next_month,
                                   day_one,
                                   day_two)
        """Четный месяц"""
        if current_month % 2 == 0:
            return filter_birthday(current_day,
                                   current_month,
                                   next_month,
                                   day_one - 1,
                                   day_two - 1)


class AddressBookView(ListAPIView):
    """Create address book view."""

    queryset = CustomUser.objects.all().order_by('last_name')
    serializer_class = AddressBookSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = AddressBookSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['last_name', 'job_title']
