from rest_framework.pagination import PageNumberPagination


class FriendPageNumberPagination(PageNumberPagination):
    page_size = 10