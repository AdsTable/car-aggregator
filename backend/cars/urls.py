from django.urls import path
from cars.views import OfferListView

urlpatterns = [
    path('list', OfferListView.as_view(), name='offer-list')
]