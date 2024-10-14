from django.urls import path
from .views import home, RegisterView, MainPageView, CustomLoginView

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('', MainPageView.as_view(), name='main'),
     path('login/', CustomLoginView.as_view(), name='login'),
]