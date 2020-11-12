from rest_framework import serializers
from .models import Offer

class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        exclude = ('primary_damage', 'secondary_damage', 'drive', 'body_style', 'fuel')
    
    def to_internal_value(self, data):
        data['images'] = data['images'][0]
        return data