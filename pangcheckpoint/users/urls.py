from django.urls import path
from .views import home, RegisterView, MainPageView, CustomLoginView
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('', home, name='users-home'),  # Home page
    path('register/', RegisterView.as_view(), name='users-register'),  # Registration page
    path('login/', CustomLoginView.as_view(), name='login'),  # Login page
    path('main/', MainPageView.as_view(), name='main'),  # Main page after login
    
]
