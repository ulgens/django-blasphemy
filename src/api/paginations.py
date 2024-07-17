from rest_framework.pagination import CursorPagination as BasePagination


class CursorPagination(BasePagination):
    ordering = "-id"
    max_page_size = 100
