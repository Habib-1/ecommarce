from django.db import transaction
from django.db.models import F
from .models import CartItem

def add_to_cart(cart, product, quantity, size=None, color=None):
    with transaction.atomic():
        item, created = CartItem.objects.select_for_update().get_or_create(
            cart=cart,
            product=product,
            size=size,
            color=color,
            defaults={"quantity": quantity},
        )
        if not created:
            item.quantity = F("quantity") + quantity
            item.save(update_fields=['quantity'])
            item.refresh_from_db()
        return item  
