from django.contrib import admin

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "category", "description", "image"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
