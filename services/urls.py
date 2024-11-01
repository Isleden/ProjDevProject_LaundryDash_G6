# services/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('services/', views.services, name='services'),  # Services page
    path('account/', views.account, name='account'),  # Account page
    path('laundry_pickup/', views.laundry_pickup, name='laundry_pickup'),  # Laundry pickup page
    path('wash_fold/', views.wash_fold, name='wash_fold'),  # Wash & fold page
    path('bulk_discount/', views.bulk_discount, name='bulk_discount'),  # Bulk discount page
    path('dry_cleaning/', views.dry_cleaning, name='dry_cleaning'),  # Dry cleaning page
    path('book_pickup/', views.book_pickup, name='book_pickup'),  # New booking URL
    path('success/', views.success_page, name='success_page'),
]
