from rest_framework.routers import DefaultRouter
from .views import ShippingAddressViewset,OrderViewSet

router=DefaultRouter()
router.register(r'shipping-address',ShippingAddressViewset,basename="shipping-address")
router.register(r"orders", OrderViewSet, basename="orders")

urlpatterns = router.urls
