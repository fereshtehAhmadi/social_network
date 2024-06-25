from tools.django.pagination import BasePagination


class StandardPaginationClass(BasePagination):
    page_size = 10
    max_limit = 20
