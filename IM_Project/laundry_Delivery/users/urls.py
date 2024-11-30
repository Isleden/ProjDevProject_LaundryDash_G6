from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('home', views.index, name = 'home'),
    path('about', views.about, name='about'),
    path('services', views.services, name="services"),
    path('main',views.home, name = 'main'),
    path('order',views.order, name = 'order'),
    path('login', views.login_view, name='login'),
    path('register', views.signup_view, name='register'),
    path('ord-history', views.ord_history, name='ord-history'), 
    path('get-services/', views.get_services, name='get_services'),
    path('edit-profile/', views.edit_customer_profile, name='edit_customer_profile'), 
    path('edit-business-profile/', views.edit_business_profile, name='edit_business_profile'),
    path('order/submit/', views.order_submit, name='order_submit'),  # Added this line for order_submit
    path('driver_dashboard', views.driver_dashboard, name='driver_dashboard'), 
    path('add-business/', views.add_business, name='add_business'),
    path('add-service/', views.add_service, name='add_service'),
    path('business_dashboard', views.business_dashboard, name='business_dashboard'), 
    path('delete-business/<int:business_id>/', views.delete_business, name='delete_business'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('order/update-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('driver_DelivHistory', views.deliv_history, name='driver_DelivHistory'), 

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)