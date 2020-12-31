from django.urls import path
from cars.views import MappingData, OfferListView, OfferRetrieveView, run_spider, available_models_for_brand, \
    available_brands_for_type, get_jobs, get_job, SimiliarVehicle, SendEmailView

urlpatterns = [
    path('list', OfferListView.as_view(), name='offer-list'),
    path('<int:pk>', OfferRetrieveView.as_view()),
    path('similiar/<int:id>', SimiliarVehicle.as_view(), name="similiar-vehicle"),
    path('map', MappingData.as_view(), name="mapping-data"),
    path('map/type/<str:vehicle_type>', available_brands_for_type, name="map-type"),
    path('map/<str:brand>', available_models_for_brand, name='map-brand'),
    path('scraper/jobs', get_jobs, name="scrapy-jobs"),
    path('scraper/job/<str:id>', get_job, name="scrapy-job"),
    path('scraper/start/<str:spider>', run_spider, name="run-spider"),
    path('sendform', SendEmailView.as_view(), name="send-form")
]