from django.contrib import admin

from .models import Warehouse, StockItem


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location", "manager")


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "warehouse",
        "book_id",
        "sku",
        "quantity",
        "reserved_quantity",
    )
    search_fields = ("sku",)