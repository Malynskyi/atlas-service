from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import WarehouseViewSet, StockItemViewSet

router = DefaultRouter()
router.register("warehouses", WarehouseViewSet, basename="warehouse")
router.register("stock", StockItemViewSet, basename="stock")

urlpatterns = [
    path("", include(router.urls)),
]