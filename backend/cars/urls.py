from django.urls import path
from cars.views import OfferListView, OfferRetrieveView, count_available_fields,available_models_for_brand 

urlpatterns = [
    path('list', OfferListView.as_view(), name='offer-list'),
    path('<int:pk>', OfferRetrieveView.as_view()),
    path('map', count_available_fields, name='map-fields'),
    path('map/<str:brand>', available_models_for_brand, name='map-brand')
]