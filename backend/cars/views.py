from django.shortcuts import render
from cars.serializers import OfferSerializer, OfferItemSerializer, ContactFormSerializer
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
from django.core import mail
from rest_framework import status

scraper = Scraper()


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CarFilterSet(django_filters.FilterSet):
    brand = django_filters.CharFilter(field_name='brand', lookup_expr="istartswith")
    model = django_filters.CharFilter(field_name='model', lookup_expr="istartswith")
    vin = django_filters.CharFilter(field_name='vin', lookup_expr="iexact")
    fuel = CharInFilter(field_name='fuel', lookup_expr="in")
    damage = CharInFilter(field_name='primary_damage', lookup_expr="in")
    transmission = CharInFilter(field_name="transmission", lookup_expr="in")
    bodyStyle = CharInFilter(field_name='body_style', lookup_expr="in")
    year = django_filters.RangeFilter(field_name="production_year")
    mileage = django_filters.RangeFilter(field_name="mileage")
    auction_site = django_filters.CharFilter(field_name='auction_site', lookup_expr="iexact")
    vehicle_type = django_filters.CharFilter(field_name='vehicle_type', lookup_expr="iexact")
    include_closed = django_filters.BooleanFilter(field_name="closed", method="filter_closed")
    drive = CharInFilter(field_name="drive", lookup_expr="in")
    # location = CharInFilter(field_name="location", lookup_expr="in")

    class Meta:
        model = Offer
        fields = ['brand', 'model', 'vin', 'fuel', 'damage', 'transmission', 'bodyStyle', 'year', 'mileage', 'auction_site', 'vehicle_type', 'include_closed', 'drive']

    def filter_closed(self, queryset, name, value):
        ''' include closed 
            if true: show all offers
            if false: hide closed offers
        '''
        if not value: 
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


class SendEmailView(APIView):

    def post(self, request):
        car = OfferSerializer(request.data['car']).data
        form = ContactFormSerializer(request.data['form']).data

        body = f"""
Klient: {form['fullname']}, 
Telefon: {form['phoneNumber']}
========================================================
Strona aukcyjna: {car['auction_site']}
Numer oferty #{car['offerId']} 
Marka i model: {car['brand']} {car['model']} 
========================================================
Wiadomość od klienta:
{form['message']}
        """

        msg = mail.EmailMessage(
            subject=f"Zapytanie o oferte [{car['brand']} {car['model']}][{car['auction_site']}][#{car['offerId']}]",
            from_email=form['email'],
            body=body,
            to=['iaaicarsearch@gmail.com'],
            reply_to=[form['email']]
        )

        msg.send()

        return Response(status=status.HTTP_202_ACCEPTED)


def get_available_options_for_field_with_count(field):
    return list(Offer.objects.values(value=F(field)).filter(value__isnull=False).annotate(count=Count('value')).order_by("value"))


def get_models_for_brand_with_count(brand):
    return list(Offer.objects.filter(brand=brand).values(value=F('model')).annotate(count=Count('value')))


def get_available_options_for_field(field):
    options = list(Offer.objects.values_list(field, flat=True).distinct().order_by(field))
    return list(filter(None, options))


def get_models_for_brand(car_type, brand):
    # TODO: REFACTOR THIS IF ELSE LOGIC
    if car_type and brand:
        models = list(Offer.objects.filter(brand=brand, vehicle_type=car_type).values_list('model', flat=True).distinct().order_by('model'))
    elif car_type and not brand:
        models = list(
            Offer.objects.filter(vehicle_type=car_type).values_list('model', flat=True).distinct().order_by('model'))
    elif not car_type and brand:
        models = list(
            Offer.objects.filter(brand=brand).values_list('model', flat=True).distinct().order_by('model'))
    else:
        models = list(
            Offer.objects.values_list('model', flat=True).distinct().order_by('model'))
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
            'vehicle_type': get_available_options_for_field('vehicle_type'),
        }
        return Response(data=data)

class FindModels(APIView):

    # @method_decorator(cache_page(6))
    def get(self, request):
        car_type = request.GET.get('type')
        car_brand = request.GET.get('brand')
        models = get_models_for_brand(car_type, car_brand)
        return Response(data=models)



class SimiliarVehicle(APIView):

    @method_decorator(cache_page(60*60*24*7))
    def get(self, request, id):
        similars = []
        offer = Offer.objects.get(id=id)
        brand, model = offer.brand, offer.model
        most_specific = Offer.objects.filter(model=model).exclude(id=id)
        
        for car in most_specific.iterator():
            if len(similars) == 4:
                return Response(data=similars)
            similars.append(OfferSerializer(car).data)

        brand_specific = Offer.objects.filter(brand=brand).exclude(id=id)

        for car in brand_specific.iterator():
            if len(similars) == 4:
                return Response(data=similars)
            similars.append(OfferSerializer(car).data)

        return Response(data=similars)


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


@api_view(['GET'])
def get_all_spiders(request):
    return Response(scraper.get_all_spiders())

@api_view(['GET'])
def cancel_job(request, job_id):
    return Response(scraper.cancel_job(job_id))