import scrapy
from scrapers.items import OfferItem
from scrapy.http import FormRequest
from pprint import pprint
import json
from datetime import datetime
from cars.models import Offer


class CopartSpider(scrapy.Spider):
    name = "copart_update"
    start_urls = [f"https://www.copart.com/public/data/lotdetails/solr/{x}" for x in list(Offer.objects.filter(sold=False).values_list('offerId', flat=True))]


    def parse(self, response):
        data = response.json()['data']['lotDetails']

        car = OfferItem()
        car['offerId'] = data['ln']
        car['sold'] = data['lotSold']
        car['current_price'] = data['hb']
        yield car
   




