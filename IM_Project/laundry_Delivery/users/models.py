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

class BusinessOwner(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='business_owner_profile')
    owner_name = models.CharField(max_length=50)

class Business(models.Model):
    business_owner = models.ForeignKey(BusinessOwner, on_delete=models.CASCADE, related_name='business_owner')
    business_name = models.CharField(max_length=100)
    business_address = models.TextField()
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)


    def __str__(self):
        return f"Business: {self.business_name} (Owner: {self.business_owner.owner_name})"

class Service(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="service_business")
    service_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    light_tendency_price = models.FloatField(default=0) 
    light_tendency_minimum = models.FloatField(default=0)
    light_tendency_maximum = models.FloatField(default=0)
    medium_tendency_price = models.FloatField(default=0)
    medium_tendency_minimum = models.FloatField(default=0)
    medium_tendency_maximum = models.FloatField(default=0)
    heavy_tendency_price = models.FloatField(default=0)
    heavy_tendency_minimum = models.FloatField(default=0)
    heavy_tendency_maximum = models.FloatField(default=0)

class Order(models.Model):
    STATUS_CHOICES = [
        ('looking_for_driver', 'Looking for Driver'),
        ('driver_on_the_way_to_pickup', 'Driver on the way to pickup'),
        ('driver_on_the_way_to_laundry', 'Driver on the way to laundry'),
        ('laundry_received', 'Laundry received'),
        ('laundry_cleaning', 'Laundry cleaning'),
        ('driver_on_the_way_to_customer', 'Driver on the way to customer'),
        ('delivered', 'Delivered'),
        ('finished', 'Finished'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    ordered_from_business = models.ForeignKey(Business, on_delete=models.CASCADE, null=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=False)
    upper_body_clothes = models.IntegerField(default=0)
    lower_body_clothes = models.IntegerField(default=0)
    underwear = models.IntegerField(default=0)
    other_stuff = models.IntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='looking_for_driver')

    def __str__(self):
        return f"Order {self.id} - Total Price: {self.total_price}"
