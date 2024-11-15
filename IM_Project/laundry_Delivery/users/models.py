# models.py

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
