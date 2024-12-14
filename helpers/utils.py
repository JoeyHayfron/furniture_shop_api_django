from rest_framework.pagination import PageNumberPagination


class FSPageNumberPagination(PageNumberPagination):
    page_size = 25
