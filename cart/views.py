from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import Cart,CartItem
from .serializers import CartItemSerializer,CartSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import F,Sum,DecimalField
from .services import add_to_cart

class CartViewSet(viewsets.ModelViewSet):
    serializer_class=CartSerializer
    permission_classes=[IsAuthenticated]
    pagination_class=None

    def get_queryset(self):
        return (
            Cart.objects.filter(customer__user=self.request.user,is_active=True)
            .annotate(
                total_items=Sum("items__quantity"),
                total_price=Sum(
                    F("items__quantity")*F("items__product__price"),
                    output_field=DecimalField(),
                )
            )
            .prefetch_related("items__product__images")
            .select_related("customer__user")
    
        )
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

    def get_serializer_context(self):
        return {"request": self.request}

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class=None

    def get_queryset(self):
        return (
            CartItem.objects.filter(cart__customer__user=self.request.user, cart__is_active=True)
            .select_related("product")
            .prefetch_related("product__images")
        )
    def get_serializer_context(self):
        return {"request": self.request}
    
    def create(self, request, *args, **kwargs):
        # get validated data first
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart, _ = Cart.objects.get_or_create(customer=self.request.user.customer, is_active=True)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        size = serializer.validated_data.get('size')
        color = serializer.validated_data.get('color')

        # use your add_to_cart service
        item = add_to_cart(cart, product, quantity, size, color)

        # serialize the created/updated item
        output_serializer = self.get_serializer(item)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)