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

class AiiaSpider(scrapy.Spider):
    name = "aiia"
    page = 0
    link = "https://aiia.pl"

    def start_requests(self):
        return [FormRequest('https://aiia.pl/pojazdy', formdata={'this_week':'W+tym+tygodniu'}, callback=self.setUp)]

    def setUp(self, response):
        yield scrapy.Request('https://aiia.pl/pojazdy', callback=self.parse)
        


    def parse(self, response):
        carLinks = response.css('td.text_left > a::attr("href")').getall()

        for car in carLinks:
            yield scrapy.Request(f"{self.link}{car}", callback=self.parseCar)


        isNextPage = response.css('a:contains("Następna")::attr(href)').get()
        if isNextPage:
            yield scrapy.Request(f"{self.link}/pojazdy{isNextPage}", callback=self.parse)


    def parseCar(self, response):
        pass


