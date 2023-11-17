from datetime import datetime

from django.db.models import Sum
from django.http import JsonResponse
from django.utils.timezone import make_aware
from django.utils.translation import gettext
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet

from .models import Category, Item, Order, Product
from .serializers import CategorySerializer, OrderSerializer, ProductSerializer
from .utils import DefaultPagination, IsClient, IsVendor


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsVendor]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrderViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    permission_classes = [IsAuthenticated, IsClient]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ["list"]:
            return [permission() for permission in [IsVendor]]
        else:
            return super().get_permissions()

    def create(self, request, *args, **kwargs):
        # create Order
        cart = request.data.pop("cart")
        request.data.update({"client": self.request.user.id})
        response = super().create(request, *args, **kwargs)

        # add items from cart to Order
        new_order = Order.objects.get(id=response.data["id"])
        items, items_ids = [], []
        for item in cart:
            created_item = Item.objects.create(
                product_id=item["product"],
                quantity=item["quantity"],
                price=item["price"],
            )
            items_ids.append(created_item.id)
            items.append(created_item.__str__())
        new_order.items.set(items_ids)

        # send confirmation email
        new_order.send_confirmation_mail()

        return JsonResponse(
            data={
                gettext("Total price"): new_order.price_total,
                gettext("Payment to"): new_order.payment_to,
            }
        )


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsVendor]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return []
        else:
            return super().get_permissions()

    def list(self, request, *args, **kwargs):
        query = self.request.query_params

        # filter response
        if "name" in query.keys():
            self.queryset = self.queryset.filter(name__icontains=query.get("name"))
        if "category" in query.keys():
            self.queryset = self.queryset.filter(
                category__name__iexact=query.get("category")
            )
        if "description" in query.keys():
            self.queryset = self.queryset.filter(
                description__icontains=query.get("description")
            )
        if "price" in query.keys():
            self.queryset = self.queryset.filter(price=query["price"])

        # sort response
        if "sort" in query.keys():
            self.queryset = self.queryset.order_by(query["sort"])

        return super().list(request, *args, **kwargs)


class StatsViewSet(ViewSet, ListModelMixin):
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated, IsVendor]
    queryset = Product.objects.all()
    items = Item.objects.prefetch_related("product")

    def list(self, request, *args, **kwargs):
        query = self.request.query_params

        # filter items to dates given in params
        if "from" in query.keys():
            date_from = make_aware(datetime.strptime(query["from"], "%d-%m-%Y"))
            self.items = self.items.filter(created_at__gte=date_from)
        if "to" in query.keys():
            date_from = make_aware(datetime.strptime(query["to"], "%d-%m-%Y"))
            self.items = self.items.filter(created_at__lte=date_from)

        # sort products by most popular items
        stats = []
        for product in self.queryset:
            stats.append(
                {
                    "product": product.__str__(),
                    "total": self.items.filter(product_id=product.id).aggregate(
                        Sum("quantity")
                    )["quantity__sum"] or 0,
                }
            )
        stats.sort(key=lambda p: p["total"], reverse=True)

        # cut the size to fit the limit param
        if "limit" in query.keys() and (limit := int(query["limit"])) < len(stats):
            stats = stats[:limit]

        # add positioning
        for i in range(len(stats)):
            stats[i].update({"place": i + 1})

        return JsonResponse(data=stats, safe=False)
