from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import viewsets,filters
from common.pagination import MyPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
    SliderSerializer,
)

from .models import (
    Category,
    Brand,
    Product,
    Product_Image,
    Slider,
)

# Create your views here.
class CategoryView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(parent=None).prefetch_related("children")
    serializer_class=CategorySerializer
    permission_classes=[AllowAny]
    pagination_class=None
    lookup_field='slug'

    
class BrandView(viewsets.ReadOnlyModelViewSet):
    queryset=Brand.objects.all()
    serializer_class=BrandSerializer
    permission_classes=[AllowAny]
    pagination_class=None
    lookup_field='slug'


class ProductView(viewsets.ReadOnlyModelViewSet):
    queryset=Product.objects.filter(is_active=True).select_related('category','brand',).prefetch_related('images')
    serializer_class=ProductSerializer
    permission_classes=[AllowAny]
    lookup_field='slug'
    pagination_class=MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset
    # Filtering fields
    filterset_fields = ['brand__slug', 'category__slug', 'price','featured']

    # Search fields
    search_fields = ['name', 'description','brand__name','category__name',]

    # Ordering fields
    ordering_fields = ['price', 'created_at',]
    ordering = ['-created_at']

class ActiveSliderList(APIView):
    def get(self, request):
        sliders = Slider.objects.filter(is_active=True)
        serializer = SliderSerializer(sliders, many=True, context={'request': request})  # ✅ Pass request context
        return Response(serializer.data)

