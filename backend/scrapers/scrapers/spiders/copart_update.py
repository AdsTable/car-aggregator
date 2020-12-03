import scrapy
from scrapers.items import OfferItem
from scrapy.http import FormRequest
from pprint import pprint
import json
from datetime import datetime
from cars.models import Offer
from django.utils import timezone
from datetime import timedelta


class CopartSpider(scrapy.Spider):
    name = "copart_update"
    start_urls = [f"https://www.copart.com/public/data/lotdetails/solr/{x}" for x in list(Offer.objects.filter(closed=False, auction_site="copart", sold=False, sale_date__gte=timezone.now()-timedelta(weeks=1)).values_list('offerId', flat=True))]


    def parse(self, response):
        data = response.json()['data']['lotDetails']

        car = OfferItem()
        if data.get('ess') != "Pure Sale":
            car['sale_date'] = datetime.fromtimestamp(data.get('ad')/1e3) if data.get('ad') else None
        car['offerId'] = data['ln']
        car['sold'] = data['lotSold']
        car['current_price'] = data['hb']
        yield car
   




