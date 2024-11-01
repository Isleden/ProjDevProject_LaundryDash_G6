from django.db import models

class Booking(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
