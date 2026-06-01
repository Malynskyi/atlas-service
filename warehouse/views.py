import logging

from django.core.cache import cache
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Warehouse, StockItem
from .serializers import WarehouseSerializer, StockItemSerializer

logger = logging.getLogger(__name__)


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.select_related("manager").all()
    serializer_class = WarehouseSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class StockItemViewSet(viewsets.ModelViewSet):
    queryset = StockItem.objects.select_related("warehouse").all()
    serializer_class = StockItemSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        cache_key = f"stock_item_{kwargs.get('pk')}"
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info("Stock item loaded from cache")
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        return response

    @action(detail=True, methods=["post"])
    def reserve(self, request, pk=None):
        item = self.get_object()
        amount = int(request.data.get("amount", 0))

        try:
            item.reserve(amount)
            logger.info("Reserved %s items for stock item %s", amount, item.id)
            return Response(
                {"status": "reserved", "available": item.available_quantity()},
                status=status.HTTP_200_OK,
            )
        except ValueError as exc:
            logger.warning("Reserve failed: %s", exc)
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"])
    def release(self, request, pk=None):
        item = self.get_object()
        amount = int(request.data.get("amount", 0))

        try:
            item.release(amount)
            logger.info("Released %s items for stock item %s", amount, item.id)
            return Response(
                {"status": "released", "available": item.available_quantity()},
                status=status.HTTP_200_OK,
            )
        except ValueError as exc:
            logger.warning("Release failed: %s", exc)
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )