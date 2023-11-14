from rest_framework.serializers import ModelSerializer

from .models import Category, Order, Product


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "client",
            "address",
            "order_datetime",
            "payment_to",
            "products",
            "price_total",
        ]


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "category", "image", "thumbnail"]
