from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('driver', 'Driver'),
        ('business', 'Business'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

class Customer(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Customer: {self.user_profile.user.username}"

class Driver(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='driver_profile')
    vehicle_details = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)

    def __str__(self):
        return f"Driver: {self.user_profile.user.username}"

class Business(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='business_profiles')
    business_name = models.CharField(max_length=100)
    business_address = models.TextField()
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)


    def __str__(self):
        return f"Business: {self.business_name} (Owner: {self.user_profile.user.username})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    upper_body_clothes = models.IntegerField(default=0)
    lower_body_clothes = models.IntegerField(default=0)
    underwear = models.IntegerField(default=0)
    other_stuff = models.IntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.id} - Total Price: {self.total_price}"