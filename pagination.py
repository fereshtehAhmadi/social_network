from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasePagination(PageNumberPagination):
    def get_paginated_response(self, data):
        if self.request.query_params.get("page_size"):
            self.page_size = int(self.request.query_params.get("page_size"))

        return Response(
            {
                "current": self.page.number,
                "page_count": self.page.paginator.num_pages,
                "page_size": self.page_size,
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            },
            status=status.HTTP_200_OK,
        )


class StandardPagination(BasePagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10
