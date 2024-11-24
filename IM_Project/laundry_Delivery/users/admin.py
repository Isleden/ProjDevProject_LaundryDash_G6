from django.contrib import admin
from .models import UserProfile, Customer, Driver, Business
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Business)