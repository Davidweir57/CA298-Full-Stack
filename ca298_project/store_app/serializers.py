from django.urls import path, include
from .models import CaUser, Product  # Import your model
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CaUser
        fields = ['url', 'username', 'email', 'is_staff']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'picture', 'category_id', 'subcategory_id']
