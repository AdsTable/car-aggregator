import scrapy
from scrapers.items import OfferItem
from scrapy.http import FormRequest
from pprint import pprint
import json
from datetime import datetime
from dateutil import tz, parser
from cars.models import Offer
from django.utils import timezone
from datetime import timedelta


tzinfos = {"CST": tz.gettz("America/Chicago")}



class IaaIUpdateSpider(scrapy.Spider):
    name = "iaai_update"
    custom_settings = {
        "DOWNLOAD_DELAY": 0.0,
    }

    start_urls = [f"https://mapp.iaai.com/acserviceswebapi/api/GetVehicleDetailsV2/?itemId={x}&userId=&culturecode=en&devicetype=android" for x in list(Offer.objects.filter(sold=False, sale_date__gte=timezone.now()-timedelta(weeks=1)).values_list('iaaiId', flat=True))]


    def parse(self, response):
        data = response.json()
        if data.get('ErrorMessage'):
            return 

        car = OfferItem()
        car['offerId'] = int(data.get("SaleInformation").get("SaleInfo").get("StockNumber"))
        car["current_price"] = float(data["BiddingInformation"]["DecimalHighBidAmount"])
        if data["BiddingInformation"]["BuyNowPrice"]:
            car["buy_now"] = float(data["BiddingInformation"]["BuyNowOfferAmount"])

        if data.get("PrebidInformation").get("AdjustedCloseDate"):
            car["sale_date"] = parser.parse(
                f"{data['PrebidInformation']['AdjustedCloseDate']} CST", tzinfos=tzinfos
            ).astimezone(tz.gettz("Europe/Warsaw"))

        sold = data.get("PrebidInformation").get("BuyNowSold")
        if not sold: 
            sold = bool(data.get('PrebidInformation').get('TimedAuctionSoldTime'))
        
        car['sold'] = sold
        yield car

