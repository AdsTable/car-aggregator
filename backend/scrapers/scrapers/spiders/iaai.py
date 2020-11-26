import scrapy
from scrapers.items import OfferItem
from scrapy.http import FormRequest
from pprint import pprint
import json
from datetime import datetime
from scrapy.http import JsonRequest
from dateutil import tz, parser
from cars.models import Offer
import pendulum
from ..map import map_fuel, map_body, map_drive, map_damage


tzinfos = {"CST": tz.gettz("America/Chicago")}

perRequest = 100

headers = {
    "Authorization": "null:null",
    "devicetype": "android",
    "deviceid": "f6dff080d417b721",
    "apikey": "eHsbhMI5mYM:APA91bEhiEocB5DVIIhPf9iZr6-304k2ddaTAGdjbPNNESobfMqRG8gVz0x0v5L_WGxCw0meoMjlNu6MY5wR12sCRfOj_rbv2w0VZ0B4W-MlKuPsq1wHC_6ZqzRU2rNrdXgE87lmWk5c",
    "appversion": "11.51313",
    "User-Agent": "IAA Buyer/11.5 Dalvik/2.1.0 (Linux; U; Android 11; Pixel 3a Build/RP1A.201105.002)",
    "Content-Type": "application/json; charset=UTF-8",
    "Host": "mapp.iaai.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
}


def generate_week_for_date(date):
    start_week = date.start_of("week")
    end_week = date.end_of("week")
    return f"{start_week.strftime('%b %-d')} - {end_week.strftime('%b %-d')}"


def generate_week(weeks=1):
    pendulum.week_starts_at(pendulum.SUNDAY)
    pendulum.week_ends_at(pendulum.SATURDAY)
    result = []
    for week in range(0, weeks):
        result.append(generate_week_for_date(pendulum.now().add(weeks=week)))
    return result


def formdata(startIndex=1):
    return {
        "CountOfVehicles": perRequest,
        "StartIndex": startIndex,
        "Keyword": "",
        "RefinerInd": False,
        "SelectedRefiners": [
            {"RefinerTypeValue": "quicklinks", "RefinerValue": generate_week()}
        ],
        "SortRule": [{"Ascending": True, "FieldName": "livedatetime"}],
    }


class IaaISpider(scrapy.Spider):
    name = "iaai"
    index = 1
    link = "https://mapp.iaai.com/acserviceswebapi/api/Search/"
    custom_settings = {
        "DOWNLOAD_DELAY": 0.0,
    }

    def start_requests(self):
        return [
            JsonRequest(
                url=self.link, data=formdata(), headers=headers, callback=self.parse
            )
        ]

    def parse(self, response):
        data = response.json()
        offers = data["Vehicles"]

        for item in offers:
            if Offer.objects.filter(offerId=item.get("StockNumber")).exists():
                continue
            o = OfferItem()
            o["offerId"] = item.get("StockNumber")
            o["iaaiId"] = item.get("ItemId")
            o["brand"] = item.get("Make")
            o["model"] = item.get("Model")
            o["production_year"] = item.get("Year")
            o["mileage"] = int(item.get("OdometerRange"))
            o["primary_damage"] = map_damage(item.get("Damage"))
            o["secondary_damage"] = item.get("SecondaryDamage")
            o["vin"] = item.get("VIN")
            o["loss_type"] = item.get("LossType")
            o["transmission"] = item.get("Transmission", "").upper()
            o["location"] = f"{item.get('BranchName')}, {item.get('State')}"
            if item.get("AuctionTime") == "Auction Not Assigned":
                continue
            o["sale_date"] = parser.parse(
                item.get("AuctionTime"), tzinfos=tzinfos
            ).astimezone(tz.gettz("Europe/Warsaw"))
            yield scrapy.Request(
                f"https://mapp.iaai.com/acserviceswebapi/api/GetVehicleDetailsV2/?itemId={o['iaaiId']}&userId=&culturecode=en&devicetype=android",
                callback=self.parse_offer,
                headers=headers,
                cb_kwargs=dict(car=o),
            )

        if data["Vehicles"]:
            self.index += perRequest
            yield JsonRequest(
                url=self.link,
                data=formdata(self.index),
                headers=headers,
                callback=self.parse,
            )

    def parse_offer(self, response, car):
        data = response.json()
        car["current_price"] = float(data["BiddingInformation"]["DecimalHighBidAmount"])
        if data["BiddingInformation"]["BuyNowPrice"]:
            car["buy_now"] = float(data["BiddingInformation"]["BuyNowOfferAmount"])
        car["estimated_repair_cost"] = parse_currency(
            data["SaleInformation"]["EstimatedRepairCost"]
        )  # $ 3,919
        car["estimated_retail_value"] = parse_currency(
            data["SaleInformation"]["ACV"]
        )  # $ 4,532

        if data.get("PrebidInformation").get("AdjustedCloseDate"):
            car["sale_date"] = parser.parse(
                f"{data['PrebidInformation']['AdjustedCloseDate']} CST", tzinfos=tzinfos
            ).astimezone(tz.gettz("Europe/Warsaw"))

        # car vin info
        car_info = dict(
            [
                (x["Name"], x["DisplayValues"][0]["Text"])
                for x in data["VinDetails"]["VINInfo"]
                if x["DisplayValues"]
            ]
        )
        car["vehicle_type"] = car_info.get("SalvageType", "").upper()
        car["body_style"] = map_body(car_info.get("BodyStyle"))
        car["drive"] = map_drive(car_info.get(" DriveLineType"))
        car["color"] = car_info.get("Color")
        car["fuel"] = map_fuel(car_info.get("FuelType"))
        car["engine"] = car_info.get("Engine")

        sold = data.get("PrebidInformation").get("BuyNowSold")
        if not sold: 
            sold = bool(data.get('PrebidInformation').get('TimedAuctionSoldTime'))
        
        car['sold'] = sold

        # images
        if data["ImageInformation"]["images"]:
            car["thumb_image"] = data["ImageInformation"]["images"][0]["ThumbImageUrl"]
            car["images"] = [x["Url"] for x in data["ImageInformation"]["images"]]

        car["auction_site"] = "iaai"
        yield car


def parse_currency(value):
    converted = value.strip()[1:].replace(",", "")
    return float(converted) if converted else 0.0
