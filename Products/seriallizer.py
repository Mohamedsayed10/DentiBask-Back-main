from rest_framework import serializers
from .models import Product, Category
class ProductSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
class CategorySeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'