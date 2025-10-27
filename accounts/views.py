from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import generics,permissions
from .models import Customer
from .serializers import CustomerSerializer
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
    
def email_confirm_redirect(request, key):
    return HttpResponseRedirect(f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/")

def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )

class CustomerView(generics.RetrieveUpdateAPIView):
    serializer_class=CustomerSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.customer