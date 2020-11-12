from django.urls import path
from cars.views import OfferListView, OfferRetrieveView

urlpatterns = [
    path('list', OfferListView.as_view(), name='offer-list'),
    path('<int:pk>', OfferRetrieveView.as_view())
]