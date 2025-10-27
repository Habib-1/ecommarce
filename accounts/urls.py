from django.urls import path,include
from dj_rest_auth.registration.views import (
    VerifyEmailView,
    ResendEmailVerificationView,
    RegisterView
)
from .views import email_confirm_redirect,password_reset_confirm_redirect,CustomerView,CustomRegisterView

from dj_rest_auth.views import ( 
    LoginView,LogoutView,UserDetailsView,
    PasswordChangeView,PasswordResetView,
    PasswordResetConfirmView,
    )
urlpatterns = [
    path('register/',CustomRegisterView.as_view(),name='register'),
    path("register/verify-email/", VerifyEmailView.as_view(), name="verify_email"),
    path("register/resend-email/", ResendEmailVerificationView.as_view(), name="resend_email"),
    path("account-confirm-email/<str:key>/", email_confirm_redirect, name="account_confirm_email"),
    path("account-confirm-email/", VerifyEmailView.as_view(), name="account_email_verification_sent"),
    
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('user/',UserDetailsView.as_view(),name='user_details'),

    path('password/change/',PasswordChangeView.as_view(),name="change_password"),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password/reset/confirm/<str:uidb64>/<str:token>/",
        password_reset_confirm_redirect,
        name="password_reset_confirm",
    ),

    path('customer/profile/',CustomerView.as_view(),name="customer_details"),
    # path('', include('dj_rest_auth.urls')),
    # path('registration/', include('dj_rest_auth.registration.urls'))

]