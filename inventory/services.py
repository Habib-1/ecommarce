from django.db import transaction
from catalog.models import Product
from inventory.models import StockLog

def stock_update(product,change_type,quantity,note='', flag=True):
    with transaction.atomic():
        if change_type == 'purchase' :
            product.stock += quantity
        elif change_type == 'return' :
            product.stock += quantity
        elif change_type == 'sale' :
            if product.stock < quantity :
                raise ValueError("Not enough stock available for sale")
            product.stock -= quantity

        elif change_type=='manual_adjustment' :
            product.stock += quantity

        else :
            raise ValueError(f"Invalid change_type: {change_type}")
        
        product.save()

        if flag and change_type in ['sale','return',]:
            StockLog.objects.create(
                product=product,
                change_type=change_type,
                quantity=quantity,
                note=note,
                )