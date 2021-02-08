# car-aggregator [![Coverage Status](https://coveralls.io/repos/github/ronek22/car-aggregator/badge.svg?branch=master)](https://coveralls.io/github/ronek22/car-aggregator?branch=master)
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

### Generate self-signed certificate
Command to generate self-signed certificate
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ~/car-aggregator/frontend/nginx/nginx-selfsigned.key -out ~/car-aggregator/frontend/nginx/nginx-selfsigned.crt;
```
