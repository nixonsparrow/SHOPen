from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Category, Order, Product
from .serializers import CategorySerializer, OrderSerializer, ProductSerializer


class CategoryViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrderViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ProductViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
