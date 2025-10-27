from rest_framework.decorators import action
from rest_framework import viewsets,status
from rest_framework.response import Response
from .serializers import ShippingAddressSerializer,OrderSerializer,OrderItemSerializer
from .models import ShippingAddress,Order,OrderItem
from rest_framework.permissions import IsAuthenticated
from .services import create_order_from_cart
# Create your views here.


class ShippingAddressViewset(viewsets.ModelViewSet):
    serializer_class=ShippingAddressSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return (
            ShippingAddress.objects.filter(customer__user=self.request.user)
            .select_related('customer','customer__user')
        )
    
    def perform_create(self, serializer):
        address=serializer.save(customer=self.request.user.customer)
        ShippingAddress.objects.filter(customer=self.request.user.customer).exclude(pk=address.pk).update(is_default=False)
        address.is_default = True
        address.save(update_fields=["is_default"])  
            

    @action(detail=False, methods=["get"], url_path="active")
    def active_address(self, request):
        address = (
            ShippingAddress.objects.filter(
                customer__user=request.user, is_default=True
            )
            .select_related("customer__user")
            .first()
        )
        if not address:
            return Response(
                {"detail": "No active shipping address found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)       



class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer__user=self.request.user).prefetch_related("items", "items__product__images")
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def create(self, request, *args, **kwargs):
        try:
            order = create_order_from_cart(request.user.customer)
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel_order(self, request, pk=None):
        order = self.get_object()

        if order.order_status in ["shipped", "delivered", "cancelled"]:
            return Response(
                {"detail": "This order cannot be cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.order_status = "cancelled"
        order.save(update_fields=["order_status"])

        return Response(
            {"detail": "Order cancelled successfully.", "order_id": order.id},
            status=status.HTTP_200_OK
        )