from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Warehouse(models.Model):
    name = models.CharField(_("warehouse name"), max_length=255)
    location = models.CharField(_("location"), max_length=255)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="warehouses",
    )

    class Meta:
        verbose_name = _("warehouse")
        verbose_name_plural = _("warehouses")

    def __str__(self):
        return self.name


class StockItem(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="stock_items",
    )
    book_id = models.PositiveIntegerField(_("book id"))
    sku = models.CharField(_("sku"), max_length=100, unique=True)
    quantity = models.PositiveIntegerField(_("quantity"), default=0)
    reserved_quantity = models.PositiveIntegerField(_("reserved quantity"), default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("stock item")
        verbose_name_plural = _("stock items")
        indexes = [
            models.Index(fields=["book_id"]),
            models.Index(fields=["sku"]),
        ]

    def available_quantity(self):
        return self.quantity - self.reserved_quantity

    def reserve(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

        if amount > self.available_quantity():
            raise ValueError("Not enough stock available")

        self.reserved_quantity += amount
        self.save(update_fields=["reserved_quantity", "updated_at"])

    def release(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

        if amount > self.reserved_quantity:
            raise ValueError("Cannot release more than reserved")

        self.reserved_quantity -= amount
        self.save(update_fields=["reserved_quantity", "updated_at"])

    def __str__(self):
        return f"{self.sku} - {self.available_quantity()} available"
