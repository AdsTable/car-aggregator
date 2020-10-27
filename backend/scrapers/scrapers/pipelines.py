# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from django.db.utils import IntegrityError


class ScrapersPipeline:
    def process_item(self, item, spider):
        try:
            item.save()
        except IntegrityError:
            print("INTEGRITY ERROR")
        
        return item
