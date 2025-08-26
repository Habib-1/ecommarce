from django.db import models
from order.models import Order
# Create your models here.

class Payment(models.Model):
    METHODS = [
        ("cash_on_delivery", "Cash on Delivery"),
        ("stripe", "Stripe"),
        ("sslcommerz", "SSLCommerz"),
        ("paypal", "PayPal"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.CharField(max_length=50, choices=METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    paid_at = models.DateTimeField(null=True, blank=True)