from rest_framework import serializers

from .models import Offer, Product


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):

    offers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "offers"]


class ProductDetailSerializer(ProductListSerializer):

    offers = OfferSerializer(many=True, read_only=True)
