from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, OrderViewSet, ProductViewSet, StatsViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"products", ProductViewSet)
router.register(r"stats", StatsViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
