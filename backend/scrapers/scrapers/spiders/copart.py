import scrapy
from scrapers.items import OfferItem
from scrapy.http import FormRequest
from pprint import pprint
import json
from datetime import datetime

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
        print(f"PAGE: {self.page} | ITEMS: {len(content)}")

        for item in content:
            o = OfferItem()
            o['offerId'] = item.get('ln')
            o['brand'] = item.get('mkn')
            o['model'] = item.get('lm')
            o['production_year'] = item.get('lcy')
            o['mileage'] = int(item.get('orr'))
            o['primary_damage'] = item.get('dd')
            o['secondary_damage'] = item.get('bndc')
            o['estimated_retail_value'] = int(item.get('la'))
            o['vin'] = item.get('fv')
            o['drive'] = item.get('drv')
            o['body_style'] = item.get('bstl')
            # o['vehicle_type'] = item['']
            o['fuel'] = item.get('ft')
            o['engine'] = item.get('egn')
            o['transmission'] = item.get('tmtp')
            # o['color'] = item['']
            o['location'] = item.get('syn')
            o['sale_date'] = datetime.fromtimestamp(item.get('ad')/1e3) if item.get('ad') else None
            # o['sold'] = False
            o['current_price'] = item.get('hb')
            yield o



        if content:
            self.page+=1
            yield FormRequest(self.link, formdata=formdata(self.page), callback=self.parse)




