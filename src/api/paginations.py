from rest_framework.pagination import CursorPagination as BasePagination

__all__ = ("CursorPagination",)


class CursorPagination(BasePagination):
    ordering = "-id"
    max_page_size = 100
