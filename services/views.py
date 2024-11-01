# services/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Booking  # Make sure to import your Booking model

def home(request):
    return render(request, 'services/home.html')

def services(request):
    return render(request, 'services/services.html')

def account(request):
    return render(request, 'services/account.html')

# Existing views for each individual service
def laundry_pickup(request):
    return render(request, 'services/laundry_pickup.html')

def wash_fold(request):
    return render(request, 'services/wash_fold.html')

def bulk_discount(request):
    return render(request, 'services/bulk_discount.html')

def dry_cleaning(request):
    return render(request, 'services/dry_cleaning.html')

def success_page(request):
    return render(request, 'services/success_page.html')

# New view for booking a pickup
def book_pickup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        pickup_date = request.POST.get('pickup_date')
        pickup_time = request.POST.get('pickup_time')
        
        # Save to the database or process as needed
        booking = Booking(name=name, address=address, pickup_date=pickup_date, pickup_time=pickup_time)
        booking.save()
        
        # Redirect to a success page or back to the main page
        return redirect('success_page')  # Update with your success page URL or name

    return render(request, 'services/book_pickup.html')  # Template for the booking form


