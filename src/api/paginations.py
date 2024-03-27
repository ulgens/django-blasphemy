from rest_framework.pagination import LimitOffsetPagination as BasePagination


class LimitOffsetPagination(BasePagination):
    default_limit = 10
    max_limit = 50
