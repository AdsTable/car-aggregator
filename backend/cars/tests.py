from typing import OrderedDict

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cars.models import Offer


def offer_to_cmp(car: OrderedDict):
    return f"{car.get('offerId')} {car.get('brand')} {car.get('model')}"


class CarTestCase(APITestCase):
    def setUp(self):
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
                      current_price=22121.00),
                Offer(id=9, offerId=9, brand='Chevrolet', model='Corvette', production_year=2015, sold=False,
                      current_price=150000.0),
                Offer(id=10, offerId=10, brand='Mazda', model='MX-5', production_year=2020, sold=False,
                      current_price=100000.0),
                Offer(id=11, offerId=11, brand='Porsche', model='911', production_year=2003, sold=False,
                      current_price=180000.0),
            ]
        )

    def test_get_cars_default_sorting(self):
        # default sorted by offerId descending
        response = self.client.get(reverse('offer-list'))
        results = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 11)
        self.assertEqual(len(results), 10)
        self.assertEqual(offer_to_cmp(results[0]), '11 Porsche 911')
        self.assertEqual(offer_to_cmp(results[-1]), '2 Mazda 5')

    def test_get_cars_sort_by_current_price(self):
        response = self.client.get(f"{reverse('offer-list')}?ordering=-current_price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(offer_to_cmp(response.data['results'][0]), '11 Porsche 911')

    def test_get_cars_filter_by_brand(self):
        response = self.client.get(f"{reverse('offer-list')}?brand=mazda")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        all_brands = set(x.get('brand') for x in data['results'])
        self.assertEqual(data['count'], 3)
        self.assertEqual(len(all_brands), 1)
        self.assertTrue('Mazda' in all_brands)

    def test_get_car_detail(self):
        response = self.client.get(reverse('offer-detail', kwargs={'pk': 5}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(offer_to_cmp(response.data), '5 Fiat Punto')
        self.assertEqual(response.data['color'], 'Blue')

    def test_get_car_that_does_not_exist(self):
        response = self.client.get(reverse('offer-detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_similiar_cars(self):
        response = self.client.get(reverse('similiar-vehicle', kwargs={'id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # similiar algorithm try to find first by model, next by brand
        self.assertEqual(len(response.data), 2)

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
        self.assertEqual(len(response.data), 1)
