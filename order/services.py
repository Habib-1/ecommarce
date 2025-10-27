from django.db import transaction
from django.db.models import F, Sum, DecimalField
from django.core.exceptions import ObjectDoesNotExist
from .models import Order, OrderItem, ShippingAddress, Variant
from cart.models import Cart

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

        shipping_charge = 60 if shipping_address.city.strip().lower() == "dhaka" else 120

        # Create Order
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount + shipping_charge,
            shipping_address=shipping_address,
            shipping_charge=shipping_charge,
            order_status="pending",
            payment_status="unpaid",
        )

        # Prepare OrderItems and update stock
        order_items = []
        for item in cart.items.all():
            product = item.product
            color = item.color
            size = item.size
            quantity = item.quantity

            try:
                # যদি variant থাকে
                variant = Variant.objects.get(
                    product=product,
                    color__name__iexact=color,
                    size__name__iexact=size
                )

                if variant.stock < quantity:
                    raise ValueError(f"Not enough stock for variant: {variant}")

                variant.stock -= quantity
                variant.save(update_fields=["stock"])

                if product.stock < quantity:
                    raise ValueError(f"Not enough stock for product: {product.name}")

                product.stock -= quantity
                product.save(update_fields=["stock"])

            except ObjectDoesNotExist:
                # ❌ যদি variant না থাকে → শুধু product.stock update হবে
                if product.stock < quantity:
                    raise ValueError(f"Not enough stock for product: {product.name}")

                product.stock -= quantity
                product.save(update_fields=["stock"])

            # ✅ Order Item তৈরি
            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    color=color,
                    size=size,
                    quantity=quantity,
                    price=product.price,  # এটা শুধু reference এর জন্য
                )
            )

        OrderItem.objects.bulk_create(order_items)

        # Deactivate cart
        cart.is_active = False
        cart.save(update_fields=["is_active"])

        return order
