from django.shortcuts import render
from cars.serializers import OfferSerializer, OfferItemSerializer
from rest_framework import generics
from cars.models import Offer
from rest_framework.filters import OrderingFilter
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.db.models import F, Q
from functools import reduce
import django_filters
from django_filters.fields import CSVWidget, MultipleChoiceField
from django_filters import rest_framework as filters
from cars.tasks import Scraper
from django.utils import timezone
from datetime import timedelta
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from conf.core import CustomOrdering

scraper = Scraper()



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
    auction_site = django_filters.CharFilter(field_name='auction_site', lookup_expr="iexact")
    vehicle_type = django_filters.CharFilter(field_name='vehicle_type', lookup_expr="iexact")
    hide_closed = django_filters.BooleanFilter(field_name="closed", method="filter_closed")

    class Meta:
        model = Offer
        fields = ['brand', 'model', 'vin', 'fuel', 'damage', 'transmission', 'bodyStyle', 'year', 'mileage', 'auction_site', 'vehicle_type', 'hide_closed']
    
    def filter_closed(self, queryset, name, value):
        ''' hide closed 
            if true: hide closed offer
            if false: show all offers
        '''
        if value: 
            return queryset.filter(
                Q(closed=False) & (Q(sale_date__gte=timezone.now()) | Q(sale_date__isnull=True))
            )
        return queryset


class OfferListView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, CustomOrdering]
    # filter_fields = ['brand', 'model', 'vin']
    filterset_class = CarFilterSet
    ordering_fields = ['current_price', 'sale_date', 'mileage', 'production_year']

class OfferRetrieveView(generics.RetrieveAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferItemSerializer

def get_available_options_for_field_with_count(field):
    return list(Offer.objects.values(value=F(field)).filter(value__isnull=False).annotate(count=Count('value')).order_by("value"))

def get_models_for_brand_with_count(brand):
    return list(Offer.objects.filter(brand=brand).values(value=F('model')).annotate(count=Count('value')))


def get_available_options_for_field(field):
    options = list(Offer.objects.values_list(field, flat=True).distinct().order_by(field))
    return list(filter(None, options))

def get_models_for_brand(brand):
    models = list(Offer.objects.filter(brand=brand).values_list('model', flat=True).distinct().order_by('model'))
    return list(filter(None, models))

def get_brand_for_type(vehicle_type):
    models = list(Offer.objects.filter(vehicle_type=vehicle_type).values_list('brand', flat=True).distinct().order_by('brand'))
    return list(filter(None, models))

class MappingData(APIView):

    @method_decorator(cache_page(60*60*24*7))
    def get(self, request):
        """
        Return dict of available values for selected fields
        """
        data = {
            'brand': get_available_options_for_field('brand'),
            'fuel': get_available_options_for_field('fuel'),
            'primary_damage': get_available_options_for_field('primary_damage'),
            'body_style': get_available_options_for_field('body_style'),
            'transmission': get_available_options_for_field('transmission'),
            'drive': get_available_options_for_field('drive'),
            'production_year': get_available_options_for_field('production_year'),
            'vehicle_type': get_available_options_for_field('vehicle_type')
        }
        return Response(data=data)


@api_view(['GET'])
def available_models_for_brand(request, brand):
    return Response(get_models_for_brand(brand))

@api_view(['GET'])
def available_brands_for_type(request, vehicle_type):
    return Response(get_brand_for_type(vehicle_type))

@api_view(['GET'])
def get_jobs(request):
    return Response(scraper.get_all_jobs())

@api_view(['GET'])
def get_job(request, id):
    return Response(scraper.get_status_of_job(id))

@api_view(['GET'])
def run_spider(request, spider):
    return Response(scraper.schedule_spider(spider))








    