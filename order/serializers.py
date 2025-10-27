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
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "product_image", "quantity","size","color","price"]
        read_only_fields = ["id", "product_name", "product_image", "price"]

    def get_product_image(self, obj):
        """
        Get the first image of the related product.
        """
        try:
            image = obj.product.images.first()  # 'images' হলো ProductImage model-এর related_name
            if image:
                request = self.context.get('request')
                return request.build_absolute_uri(image.image.url) if request else image.image.url
            return None
        except Exception:
            return None
       


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
            "shipping_charge",
            "items",
            
        ]
        read_only_fields = [
            "id",
            "order_status",
            "payment_status",
            "total_amount",
            "shipping_address",
            "shipping_charge",
            "items",
            
        ]
