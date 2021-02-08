from django.urls import path
from cars.views import MappingData, OfferListView, OfferRetrieveView, run_spider, \
    available_brands_for_type, get_jobs, get_job, SimiliarVehicle, SendEmailView, FindModels, get_all_spiders, \
    cancel_job

urlpatterns = [
    path('list', OfferListView.as_view(), name='offer-list'),
    path('<int:pk>', OfferRetrieveView.as_view(), name='offer-detail'),
    path('similiar/<int:id>', SimiliarVehicle.as_view(), name="similiar-vehicle"),
    path('models/', FindModels.as_view(), name="find-models"),
    path('map', MappingData.as_view(), name="mapping-data"),
    path('map/type/<str:vehicle_type>', available_brands_for_type, name="map-type"),
    path('scraper/spiders', get_all_spiders, name="scrapy-spiders"),
    path('scraper/jobs', get_jobs, name="scrapy-jobs"),
    path('scraper/job/<str:id>', get_job, name="scrapy-job"),
    path('scraper/job/<str:job_id>/cancel', cancel_job, name="scrapy-cancel-job"),
    path('scraper/start/<str:spider>', run_spider, name="run-spider"),
    path('sendform', SendEmailView.as_view(), name="send-form")
]