from rest_framework import serializers
from .models import Offer

class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        exclude = ('id',)
    
