from django.contrib import admin

from .models import Category, Order, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "client", "address", "order_datetime", "payment_to"]


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "quantity",
        "price",
        "category",
        "description",
        "image",
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
