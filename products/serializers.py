from rest_framework.serializers import ModelSerializer

from .models import Category, Item, Order, Product


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "product", "quantity", "price")


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "client",
            "items",
            "address",
            "order_datetime",
            "payment_to",
        )


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "category", "image", "thumbnail")
