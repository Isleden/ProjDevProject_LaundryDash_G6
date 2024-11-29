from django.contrib import admin
from .models import UserProfile, Customer,Order, Driver, Business, BusinessOwner, Service
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(BusinessOwner)
admin.site.register(Business)
admin.site.register(Order)
admin.site.register(Service)
