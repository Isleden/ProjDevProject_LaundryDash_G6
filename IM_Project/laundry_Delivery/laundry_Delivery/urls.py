
from django.contrib import admin
from django.urls import path, include 
from users import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('users/', include('users.urls', namespace='users')),
]
