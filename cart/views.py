from django.shortcuts import render
from rest_framework import viewsets
from .models import Cart,CartItem
from .serializers import CartItemSerializer,CartSerializer
from rest_framework.permissions import IsAuthenticated

class CartViewSet(viewsets.ModelViewSet):
    serializer_class=CartSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(customer__user=self.request.user,is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class=CartItemSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__customer__user=self.request.user, cart__is_active=True)
    
    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(customer=self.request.user.customer, is_active=True)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            serializer.save(cart=cart)