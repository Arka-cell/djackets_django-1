from rest_framework import serializers

from .models import Order, OrderItem, PersonalInfos

from product.serializers import ProductSerializer


class MyOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
        )


class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "name",
            "items",
        )


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "name",
            "user",
            "created_at",
            "items"
        )

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order


class PersonalInfosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfos
        read_only_fields = ("confirmed", "user")
        fields = (
            "first_name",
            "last_name",
            "phone",
            "instagram",
            "instagram_followers",
            "facebook",
            "facebook_followers",
            "tiktok",
            "tiktok_followers",
            "youtube",
            "youtube_followers",
            "confirmed",
            "user"
        )

