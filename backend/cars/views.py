from django.shortcuts import render
from cars.serializers import OfferSerializer
from rest_framework import generics
from cars.models import Offer
import django_filters.rest_framework
from rest_framework.filters import OrderingFilter

class OfferListView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
    filter_fields = ['brand']
    ordering_fields = ['current_price']
    