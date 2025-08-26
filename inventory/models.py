from django.db import models
from catalog.models import Product
from common.models import BaseModel
# Create your models here.
class StockLog(BaseModel):
    CHANGE_TYPE_CHOICES = [
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('return', 'Return'),
        ('manual_adjustment', 'Manual Adjustment'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_logs')
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE_CHOICES)
    quantity = models.IntegerField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.change_type} ({self.quantity})"