from rest_framework.utils.urls import remove_query_param, replace_query_param
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from collections import OrderedDict
from math import ceil

DEFAULT_PAGE = 0
DEFAULT_PAGE_SIZE = 20


class MyPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'size'
    
    def get_paginated_response(self, data):
        return Response({
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
            'size': int(self.request.GET.get('size', self.page_size)),
            'count': self.page.paginator.count,
            'lastPage': ceil(self.page.paginator.count / int(self.request.GET.get('size', self.page_size))),
            'results': data
        })

class LimitPagination(LimitOffsetPagination):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('limit', self.limit),
            ('results', data)
        ]))

    def get_next_link(self):
        if self.offset + self.limit >= self.count:
            return None

        url = self.request.get_full_path()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        offset = self.offset + self.limit
        return replace_query_param(url, self.offset_query_param, offset)

    def get_previous_link(self):
        if self.offset <= 0:
            return None

        url = self.request.get_full_path()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        if self.offset - self.limit <= 0:
            return remove_query_param(url, self.offset_query_param)

        offset = self.offset - self.limit
        return replace_query_param(url, self.offset_query_param, offset)



