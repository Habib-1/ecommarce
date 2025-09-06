
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/',include('accounts.urls')),
    path('api/',include('catalog.urls')),
    path('api/',include('cart.urls')),
    path('api/',include('order.urls')),
    path('api/',include('payment.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
