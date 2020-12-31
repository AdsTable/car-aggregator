from abc import ABC

from rest_framework import serializers
from .models import Offer


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        exclude = ('primary_damage', 'secondary_damage', 'drive', 'body_style')
    
    def to_internal_value(self, data):
        data['images'] = data['images'][0]
        return data


class OfferItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        exclude = ('id', )


class ContactFormSerializer(serializers.Serializer):
    email = serializers.EmailField()
    fullname = serializers.CharField()
    message = serializers.CharField()
    phoneNumber = serializers.CharField()
