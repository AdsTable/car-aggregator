from django.shortcuts import render
from cars.serializers import OfferSerializer, OfferItemSerializer
from rest_framework import generics
from cars.models import Offer
from rest_framework.filters import OrderingFilter
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import F, Q
from functools import reduce
import django_filters
from django_filters.fields import CSVWidget, MultipleChoiceField
from django_filters import rest_framework as filters

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CarFilterSet(django_filters.FilterSet):
    brand = django_filters.CharFilter(field_name='brand', lookup_expr="istartswith")
    model = django_filters.CharFilter(field_name='model', lookup_expr="istartswith")
    vin = django_filters.CharFilter(field_name='vin', lookup_expr="iexact")
    fuel = CharInFilter(field_name='fuel', lookup_expr="in")
    damage = CharInFilter(field_name='primary_damage', lookup_expr="in")
    transmission = django_filters.CharFilter(field_name='transmission', lookup_expr="iexact")
    bodyStyle = CharInFilter(field_name='body_style', lookup_expr="in")
    year = django_filters.RangeFilter(field_name="production_year")
    mileage = django_filters.RangeFilter(field_name="mileage")

    class Meta:
        model = Offer
        fields = ['brand', 'model', 'vin', 'fuel', 'damage', 'transmission', 'bodyStyle', 'year', 'mileage']


class OfferListView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
    # filter_fields = ['brand', 'model', 'vin']
    filterset_class = CarFilterSet
    ordering_fields = ['current_price']
    ordering = ['-id']

class OfferRetrieveView(generics.RetrieveAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferItemSerializer

def get_available_options_for_field_with_count(field):
    return list(Offer.objects.values(value=F(field)).filter(value__isnull=False).annotate(count=Count('value')).order_by("value"))

def get_models_for_brand_with_count(brand):
    return list(Offer.objects.filter(brand=brand).values(value=F('model')).annotate(count=Count('value')))


def get_available_options_for_field(field):
    options = list(Offer.objects.values_list(field, flat=True).distinct(field))
    return list(filter(None, options))

def get_models_for_brand(brand):
    models = list(Offer.objects.filter(brand=brand).values_list('model', flat=True).distinct('model'))
    return list(filter(None, models))

@api_view(['GET'])
def count_available_fields(request):
    data = {
        'brand': get_available_options_for_field('brand'),
        'fuel': get_available_options_for_field('fuel'),
        'primary_damage': get_available_options_for_field('primary_damage'),
        'secondary_damage': get_available_options_for_field('secondary_damage'),
        'body_style': get_available_options_for_field('body_style'),
        'transmission': get_available_options_for_field('transmission'),
        'drive': get_available_options_for_field('drive'),
        'production_year': get_available_options_for_field('production_year')
    }

    return Response(data=data)

@api_view(['GET'])
def available_models_for_brand(request, brand):
    return Response(get_models_for_brand(brand))







    