from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import CustomLoginView  
from users.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # This already includes the login path
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
