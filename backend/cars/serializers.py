from abc import ABC

from rest_framework import serializers
from .models import Offer


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        exclude = ('secondary_damage', 'drive', 'body_style', 'images')


class OfferItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        exclude = ('id', )


class ContactFormSerializer(serializers.Serializer):
    email = serializers.EmailField()
    fullname = serializers.CharField()
    message = serializers.CharField()
    phoneNumber = serializers.CharField()
