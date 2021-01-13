# car-aggregator
WebApp, Search engine for vehicle auctions from Copart and IAAI

## Technology Stack

Technology | Role
:-------------------------:|:-------------------------:
Python |  Backend Language
Django & DRF | Backend framework
Angular | Frontend framework
Celery | background task & async mechanism for Django
Scrapy | webscraping framework
Scrapyd | deploying scrapy spiders and manage them by JSON API
PostgreSQL | RDBMS
Redis | Manage Celery Task & Cache some endpoints

Thanks to Celery Beat, scheduling tasks can be done in Django Admin by intervals or cron syntax
