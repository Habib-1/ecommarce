from rest_framework import serializers
from .models import ShippingAddress,Order,OrderItem


class ShippingAddressSerializer(serializers.ModelSerializer):
    customer = serializers.EmailField(source="customer.user.email", read_only=True)
    class Meta: 
        model=ShippingAddress
        exclude=('created_at','updated_at',)
        read_only_fields=("customer",)


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "quantity", "price"]
        read_only_fields = ["id", "product_name", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_status",
            "payment_status",
            "total_amount",
            "shipping_address",
            "items",
        ]
        read_only_fields = [
            "id",
            "order_status",
            "payment_status",
            "total_amount",
            "shipping_address",
            "items",
        ]
