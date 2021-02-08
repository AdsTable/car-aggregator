from rest_framework.utils.urls import remove_query_param, replace_query_param
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from collections import OrderedDict
from math import ceil
from rest_framework.filters import OrderingFilter


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10


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


class CustomOrdering(OrderingFilter):

    def get_ordering(self, request, queryset, view):
        """
        Ordering is set by a comma delimited ?ordering=... query parameter.

        The `ordering` query parameter can be overridden by setting
        the `ordering_param` value on the OrderingFilter or by
        specifying an `ORDERING_PARAM` value in the API settings.
        """
        params = request.query_params.get(self.ordering_param)

        if params:
            fields = [param.strip() for param in params.split(',')]
            if fields: return fields

        # No ordering was included, or all the ordering fields were invalid
        return self.get_default_ordering(view)

    def filter_queryset(self, request, queryset, view):

        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            ordering.append('-id')

        if not ordering:
            ordering = ['-id']
            
        return queryset.order_by(*ordering)



