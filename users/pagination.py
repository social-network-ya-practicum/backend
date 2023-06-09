from rest_framework.pagination import PageNumberPagination


class AddressBookSetPagination(PageNumberPagination):
    page_size = 5


class UsersSetPagination(PageNumberPagination):
    page_size = 10
