from rest_framework.pagination import PageNumberPagination


class AddressBookSetPagination(PageNumberPagination):
    page_size = 5
