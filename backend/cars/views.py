from django.shortcuts import render
from cars.serializers import OfferSerializer, OfferItemSerializer
from rest_framework import generics
from cars.models import Offer
import django_filters.rest_framework
from rest_framework.filters import OrderingFilter
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import F


class OfferListView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
    filter_fields = ['brand', 'model', 'vin']
    ordering_fields = ['current_price']
    ordering = ['-id']

class OfferRetrieveView(generics.RetrieveAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferItemSerializer

def get_available_options_for_field(field):
    return list(Offer.objects.values(value=F(field)).filter(value__isnull=False).annotate(count=Count('value')).order_by("value"))

def get_models_for_brand(brand):
    return list(Offer.objects.filter(brand=brand).values(value=F('model')).annotate(count=Count('value')))

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







    