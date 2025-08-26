from django.urls import path,include
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView,LogoutView,UserDetailsView
urlpatterns = [
    # path('register/',RegisterView.as_view(),name='register'),
    # path('login/',LoginView.as_view(),name='login'),
    # path('logout/',LogoutView.as_view(),name='logout'),
    # path('user/',UserDetailsView.as_view(),name='user_details'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))

]