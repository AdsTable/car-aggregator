from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cars.models import Offer
from cars.serializers import OfferSerializer, OfferItemSerializer
from cars.utils import get_available_options_for_field, get_models_for_brand


def populate_database():
    Offer.objects.bulk_create(
        [
            Offer(id=1, offerId=1, brand='Mazda', model='3', production_year=2005, sold=False,
                  current_price=8121.00,
                  closed=False, vehicle_type='AUTOMOBILE'),
            Offer(id=2, offerId=2, brand='Mazda', model='5', production_year=2010, sold=True,
                  current_price=25000.00,
                  closed=True),
            Offer(id=3, offerId=3, brand='Volkswagen', model='Passat', production_year=2009, sold=False,
                  current_price=18551.00, auction_site="iaai"),
            Offer(id=4, offerId=4, brand='BMW', model='325i', production_year=2011, sold=False,
                  current_price=30121.00,
                  closed=True),
            Offer(id=5, offerId=5, brand='Fiat', model='Punto', production_year=1995, sold=False,
                  current_price=1121.00,
                  closed=True, color='Blue'),
            Offer(id=6, offerId=6, brand='Fiat', model='Bravo', production_year=2012, sold=False,
                  current_price=25121.00),
            Offer(id=7, offerId=7, brand='Fiat', model='Siena', production_year=1999, sold=False,
                  current_price=1500.00),
            Offer(id=8, offerId=8, brand='Chevrolet', model='Cruze', production_year=2010, sold=False,
                  current_price=22121.00, vehicle_type='AUTOMOBILE'),
            Offer(id=9, offerId=9, brand='Chevrolet', model='Corvette', production_year=2015, sold=False,
                  current_price=150000.0),
            Offer(id=10, offerId=10, brand='Mazda', model='MX-5', production_year=2020, sold=False,
                  current_price=100000.0),
            Offer(id=11, offerId=11, brand='Porsche', model='911', production_year=2003, sold=False,
                  current_price=180000.0),
        ]
    )


class UtilTestCase(TestCase):
    def setUp(self):
        populate_database()

    def test_get_available_options_for_brand(self):
        available_brands = sorted(['Fiat', 'Mazda', 'Volkswagen', 'Chevrolet', 'Porsche', 'BMW'])
        result_from_function = get_available_options_for_field('brand')
        self.assertListEqual(available_brands, result_from_function)

    def test_get_models_for_brand(self):
        mazda_models = ['3', '5', 'MX-5']
        result_from_function = get_models_for_brand('', 'Mazda')
        self.assertListEqual(mazda_models, result_from_function)

    def test_get_models_for_type(self):
        automobile_models = ['3', 'Cruze']
        result_from_function = get_models_for_brand('AUTOMOBILE', '')
        self.assertListEqual(automobile_models, result_from_function)

    def test_get_models_for_type_and_brand(self):
        automobile_mazda_models = ['3']
        result_from_function = get_models_for_brand('AUTOMOBILE', 'Mazda')
        self.assertListEqual(automobile_mazda_models, result_from_function)


class CarTestCase(APITestCase):
    def setUp(self):
        populate_database()

    def test_get_cars_default_sorting(self):
        # default sorted by id descending
        response = self.client.get(reverse('offer-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        offers_from_db = OfferSerializer(Offer.objects.all()[:10], many=True)
        self.assertEqual(response.data['results'], offers_from_db.data)

    def test_get_cars_sort_by_current_price(self):
        response = self.client.get(f"{reverse('offer-list')}?ordering=-current_price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        offers_from_db = OfferSerializer(Offer.objects.all().order_by('-current_price')[:10], many=True)
        self.assertEqual(response.data['results'], offers_from_db.data)

    def test_get_cars_filter_by_brand(self):
        response = self.client.get(f"{reverse('offer-list')}?brand=mazda")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        offers_from_db = OfferSerializer(Offer.objects.filter(brand='Mazda'), many=True)
        self.assertEqual(response.data['results'], offers_from_db.data)

    def test_get_cars_hide_closed_offers(self):
        response = self.client.get(f"{reverse('offer-list')}?include_closed=false")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        offers_from_db = OfferSerializer(Offer.objects.exclude(closed=True), many=True)
        self.assertEqual(response.data['results'], offers_from_db.data)

    def test_get_cars_show_all_offers_explicitly(self):
        response = self.client.get(f"{reverse('offer-list')}?include_closed=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        offers_from_db = OfferSerializer(Offer.objects.all()[:10], many=True)
        self.assertEqual(response.data['results'], offers_from_db.data)

    def test_get_car_detail(self):
        response = self.client.get(reverse('offer-detail', kwargs={'pk': 5}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        offer_from_db = OfferItemSerializer(Offer.objects.get(pk=5))
        self.assertEqual(response.data, offer_from_db.data)

    def test_get_car_that_does_not_exist(self):
        response = self.client.get(reverse('offer-detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_similiar_cars(self):
        response = self.client.get(reverse('similiar-vehicle', kwargs={'id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # similiar algorithm try to find first by model, next by brand
        # so all similiar cars have to have the same brand
        brand_of_selected = Offer.objects.get(id=1).brand
        amount_of_similiar = Offer.objects.filter(brand=brand_of_selected).exclude(id=1).count()

        self.assertTrue(all(x.get('brand') == brand_of_selected for x in response.data))
        self.assertEqual(len(response.data), amount_of_similiar)

    def test_get_available_models_in_database(self):
        response = self.client.get(reverse('find-models'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 11)

    def test_get_mapping_data(self):
        response = self.client.get(reverse('mapping-data'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data: dict = response.data
        should_mapped = ['brand', 'fuel', 'primary_damage', 'body_style', 'transmission', 'drive',
                         'production_year', 'vehicle_type']

        actual_keys = list(data)
        self.assertListEqual(should_mapped, actual_keys)

    def test_get_brands_by_vehicle_type(self):
        response = self.client.get(reverse('map-type', kwargs={'vehicle_type': 'AUTOMOBILE'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
