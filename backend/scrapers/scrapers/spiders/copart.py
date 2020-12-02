import scrapy
from scrapers.items import OfferItem
from scrapy.http import FormRequest
from pprint import pprint
import json
from datetime import datetime
from ..map import map_fuel, map_body, map_drive, map_damage


def formdata(page):
    return {
        'size': '100', 
        'sort': 'auction_date_type+desc,auction_date_utc+asc', 
        'filter[NLTS]': 'expected_sale_assigned_ts_utc:[NOW/DAY-1DAY+TO+NOW/DAY]',
        'page': str(page)
    }

class CopartSpider(scrapy.Spider):
    name = "copart"
    page = 0
    link = 'https://www.copart.com/public/lots/search'

    def start_requests(self):
        return [FormRequest(self.link, formdata=formdata(0), callback=self.parse)]

    def parse(self, response):
        data = json.loads(response.body)
        content = data['data']['results']['content']

        for item in content:
            o = OfferItem()
            o['offerId'] = item.get('ln')
            o['brand'] = item.get('mkn')
            o['model'] = item.get('lm')
            o['production_year'] = item.get('lcy')
            o['mileage'] = int(item.get('orr'))
            o['primary_damage'] = map_damage(item.get('dd'))
            # o['secondary_damage'] = item.get('bndc')
            o['estimated_retail_value'] = int(item.get('la'))
            o['vin'] = item.get('fv')
            o['drive'] = map_drive(item.get('drv'))
            o['body_style'] = map_body(item.get('bstl'))
            o['fuel'] = map_fuel(item.get('ft'))
            o['engine'] = item.get('egn')
            o['transmission'] = item.get('tmtp', '').upper()
            o['location'] = item.get('syn')
            if item.get('ess') != "Pure Sale":
                o['sale_date'] = datetime.fromtimestamp(item.get('ad')/1e3) if item.get('ad') else None
            o['current_price'] = item.get('hb')
            yield scrapy.Request(f"https://www.copart.com/public/data/lotdetails/solr/lotImages/{o['offerId']}/USA", callback=self.parse_images, cb_kwargs=dict(car=o),
            headers={'Host':'www.copart.com'})



        if content:
            self.page+=1
            yield FormRequest(self.link, formdata=formdata(self.page), callback=self.parse)

    def parse_images(self, response, car):
        data = response.json()
        content = data['data']['imagesList']['FULL_IMAGE']
        car['images'] = [x['url'] for x in content]
        car['thumb_image'] = content[0]['url']
        yield scrapy.Request(f"https://www.copart.com/public/data/lotdetails/solr/{car['offerId']}", callback=self.parse_details, cb_kwargs=dict(car=car),headers={'Host':'www.copart.com'})



    def parse_details(self, response, car):
        data = response.json()['data']['lotDetails']
        car['color'] = data['clr']
        car['vehicle_type'] = data.get('vehTypDesc', '').upper()
        car['sold'] = data['lotSold']
        yield car


