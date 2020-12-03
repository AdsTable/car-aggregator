# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from django.db.utils import IntegrityError
from cars.models import Offer


class ScrapersPipeline:
    def process_item(self, item, spider):
        if spider.name in ['copart_update', 'iaai_update']:
            if item['iaaiId']:
                offer = Offer.objects.get(iaaiId=item['iaaiId'])
                setattr(offer, 'closed', item['closed'])
                offer.save()
                return

            try:
                offer = Offer.objects.get(offerId=item['offerId'], auction_site=item['auction_site'])
                for k,v in item.items():
                    setattr(offer, k, v)
                offer.save()  
            except Offer.DoesNotExist:
                print("[UPDATE] Offer doesn't exist")

        elif spider.name in ['copart', 'iaai']:
            try:
                item.save()
            except IntegrityError:
                print("[NEW] Item already in database")

        return item              
        
