from django.urls import path, include
from .views import (
    CategoryView,
    BrandView,
    ProductView,
    ActiveSliderList,
)
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register(r'categories',CategoryView,basename='categories')
router.register(r'brands',BrandView,basename='brands')
router.register(r'products',ProductView, basename='products')

urlpatterns = [
    path('',include(router.urls)),
    path('sliders/', ActiveSliderList.as_view(), name='slider-list'),
]
