from django.db import transaction
from django.db.models import F
from catalog.models import Product
from inventory.models import StockLog

def stock_update(product_id,change_type,quantity,note='', flag=True):

    with transaction.atomic():
        product=Product.objects.select_for_update().get(id=product_id)
        if change_type == 'purchase' :
            product.stock = F('stock') + quantity
        elif change_type == 'return' :
            product.stock = F('stock') + quantity
        elif change_type == 'sale' :
            if product.stock < quantity :
                raise ValueError("Not enough stock available for sale")
            product.stock = F('stock') - quantity

        elif change_type=='manual_adjustment' :
            product.stock = quantity

        else :
            raise ValueError(f"Invalid change_type: {change_type}")
        
        product.save(update_fields=['stock'])
        product.refresh_from_db(fields=['stock'])

        if flag and change_type in ['sale','return',]:
            StockLog.objects.create(
                product=product,
                change_type=change_type,
                quantity=quantity,
                note=note,
                )
        return product.stock
    