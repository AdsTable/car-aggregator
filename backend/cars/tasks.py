from scrapyd_api import ScrapydAPI
from celery import shared_task


class Scraper:
    def __init__(self):
        self.client = ScrapydAPI("http://scrapyd:6800", timeout=10)
        self.project = 'default'

    def schedule_spider(self, spider_name: str):
        print(f"RUN SPIDER: {spider_name}")
        return self.client.schedule(self.project, spider_name)
    
    def cancel_job(self, job_id: str):
        return self.client.cancel(self.project, job_id)

    def get_status_of_job(self, job_id: str):
        return self.client.job_status(self.project, job_id)

    def get_all_jobs(self):
        return self.client.list_jobs(self.project)


@shared_task
def test_task():
    print('TASK RUN')

@shared_task
def run_copart_scraper_everyday():
    print('RUN COPART')
    scraper = Scraper()
    scraper.schedule_spider('copart')

@shared_task
def run_iaai_scraper_weekly():
    scraper = Scraper()
    print('RUN IAAI PER WEEK')
    scraper.schedule_spider('iaai')

@shared_task
def update_iaai():
    scraper = Scraper()
    print('RUN IAAI UPDATE')
    scraper.schedule_spider('iaai_update')

@shared_task 
def update_copart():
    scraper = Scraper()
    print('RUN COPART UPDATE')
    scraper.schedule_spider('copart_update')

