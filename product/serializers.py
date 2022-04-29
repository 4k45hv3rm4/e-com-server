from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductData
        fields = ['id', 'title', 'image', 'description', 'price']


class OrderDataSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = models.OrderData
        fields = ['id','product', 'amount', 'user']


class CartDataSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = models.CartData
        fields = ['id', 'user', 'product']
