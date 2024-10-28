from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('home', views.index, name = 'home'),
    path('about', views.about, name='about'),
    path('main',views.home, name = 'main'),
    path('order',views.order, name = 'order'),
    path('login', views.login_view, name='login'),
    path('register', views.signup_view, name='register'),
    path('ord-history', views.ord_history, name='ord-history'),  
    path('order/submit/', views.order_submit, name='order_submit'),  # Added this line for order_submit

]