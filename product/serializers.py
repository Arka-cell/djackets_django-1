from rest_framework import serializers

from .models import Category, Product, Brand


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail",
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
        )

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "image"
        ]
