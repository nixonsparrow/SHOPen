from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HomePage, OrderCreateView
from .views_api import (CategoryViewSet, OrderViewSet, ProductViewSet,
                        StatsViewSet)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"products", ProductViewSet)
router.register(r"stats", StatsViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", HomePage.as_view(), name="homepage"),
    path("create_order/", OrderCreateView.as_view(), name="create-order"),
]
