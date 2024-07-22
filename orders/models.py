from django.db import models
from django.contrib.auth import get_user_model
from .models import Product
from django.utils import timezone
from constants.constant import order_status
from utils.utils import generate_ref


User = get_user_model()


class OrderProduct(models.Model):
    product = models.ForeignKey(
        Product, related_name="order_products", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        verbose_name = "Order Product"
        verbose_name_plural = "Order Products"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.product.price
        super().save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(
        User, related_name="orders", on_delete=models.CASCADE, editable=False
    )
    products = models.ManyToManyField(Product, through="OrderProduct")
    status = models.CharField(max_length=50, choices=order_status, default="Pending")
    total_amount = models.FloatField(null=True, blank=True)
    order_ref = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.order_ref} - {self.user.username}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]
        db_table = "orders"

    def save(self, *args, **kwargs):
        self.order_ref = generate_ref()
        self.total_amount = sum(p.subtotal for p in self.products.all())
        super().save(*args, **kwargs)
