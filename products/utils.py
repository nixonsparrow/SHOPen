from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission


def get_payment_to_date(days=5):
    return (timezone.now() + timezone.timedelta(days=days)).date()


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Client").exists()


class IsVendor(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Vendor").exists()
