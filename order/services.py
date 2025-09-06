
from django.db import transaction
from django.db.models import F, Sum, DecimalField
from .models import Order, OrderItem
from cart.models import Cart
from .models import ShippingAddress

def create_order_from_cart(customer):
    with transaction.atomic():
        # Get active cart with items and products
        cart = (
            Cart.objects.filter(customer=customer, is_active=True)
            .prefetch_related("items__product")
            .first()
        )
        if not cart or not cart.items.exists():
            raise ValueError("No active cart or cart is empty.")

        # Default shipping address
        shipping_address = ShippingAddress.objects.filter(customer=customer, is_default=True).first()
        if not shipping_address:
            raise ValueError("No default shipping address found.")

        # Total price calculate using F() expressions
        total_amount = (
            cart.items.annotate(
                item_total=F("quantity") * F("product__price")
            ).aggregate(
                total=Sum("item_total", output_field=DecimalField(max_digits=10, decimal_places=2))
            )["total"]
        )

        # Create Order
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
            shipping_address=shipping_address,
            order_status="pending",
            payment_status="unpaid",
        )

        # Create OrderItems efficiently
        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            for item in cart.items.all()
        ]
        OrderItem.objects.bulk_create(order_items)

        return order
