from rest_framework import serializers

from .models import Warehouse, StockItem


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "name", "location", "manager"]


class StockItemSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        source="warehouse",
        write_only=True,
    )
    available_quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = StockItem
        fields = [
            "id",
            "warehouse",
            "warehouse_id",
            "book_id",
            "sku",
            "quantity",
            "reserved_quantity",
            "available_quantity",
            "updated_at",
        ]