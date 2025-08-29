from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import viewsets,filters
from common.pagination import MyPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
)

from .models import (
    Category,
    Brand,
    Product,
    Product_Image,
)

# Create your views here.
class CategoryView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(parent=None).prefetch_related("children")
    serializer_class=CategorySerializer
    permission_classes=[AllowAny]
    lookup_field='slug'

    
class BrandView(viewsets.ReadOnlyModelViewSet):
    queryset=Brand.objects.all()
    serializer_class=BrandSerializer
    permission_classes=[AllowAny]
    lookup_field='slug'


class ProductView(viewsets.ReadOnlyModelViewSet):
    queryset=Product.objects.filter(is_active=True).select_related('category','brand',).prefetch_related('images')
    serializer_class=ProductSerializer
    permission_classes=[AllowAny]
    lookup_field='slug'
    pagination_class=MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering fields
    filterset_fields = ['brand', 'category', 'price']

    # Search fields
    search_fields = ['name', 'description','brand__name','category__name',]

    # Ordering fields
    ordering_fields = ['price', 'created_at',]
    ordering = ['-created_at']