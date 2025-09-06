# order/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PaymentSerializer
from order.services import create_order_from_cart

class PaymentViewSet(viewsets.ViewSet):
    pass

