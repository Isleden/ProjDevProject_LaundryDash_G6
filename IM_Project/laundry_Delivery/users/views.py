from django.shortcuts import render, redirect 
from .models import Order, UserProfile, Business
from .forms import OrderForm, SignupForm, LoginForm, BusinessForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'users/index.html')

def about(request):
    return render(request, 'users/about.html')

def home(request):
    return render(request, 'users/home.html')

def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()  # Save the order
            return redirect('users:home')
    else:
        form = OrderForm()
    return render(request, 'users/order.html', {'form': form})

def ord_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)  # Filter orders for the logged-in user
    else:
        orders = []  # No orders if the user is not authenticated
    return render(request, 'users/ord-history.html', {'orders': orders})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')  # Redirect to login page after signup
    else:
        form = SignupForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Check user type and redirect accordingly
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.user_type == 'driver':
                return redirect('users:driver_dashboard')
            if user_profile.user_type == 'business':
                return redirect('users:business_dashboard')
            else:
                return redirect('users:main')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def driver_dashboard(request):
    # Placeholder for the driver's dashboard
    return render(request, 'users/driver_dashboard.html')

@login_required
def customer_dashboard(request):
    # Placeholder for the customer's dashboard
    return render(request, 'users/ord-history.html')


@login_required
def add_business(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.user_profile = UserProfile.objects.get(user=request.user)
            business.save()
            return redirect('business_list')  # Replace with your business list view or another URL
    else:
        form = BusinessForm()
    return render(request, 'users/add_business.html', {'form': form})

@login_required
def business_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    businesses = Business.objects.filter(user_profile=user_profile)
    return render(request, 'users/business_dashboard.html', {'businesses': businesses})
def order_submit(request):
    if request.method == 'POST':
        # Extract data from the form
        upper_body_clothes = int(request.POST.get('upper_body_clothes', 0))
        lower_body_clothes = int(request.POST.get('lower_body_clothes', 0))
        underwear = int(request.POST.get('underwear', 0))
        other_stuff = int(request.POST.get('other_stuff', 0))

        # Assuming fixed prices
        price_per_upper = 2  # Example price
        price_per_lower = 2  # Example price
        price_per_underwear = 5  # Example price
        price_per_other = 10  # Example price

        # Calculate total price
        total_price = (upper_body_clothes * price_per_upper) + \
                      (lower_body_clothes * price_per_lower) + \
                      (underwear * price_per_underwear) + \
                      (other_stuff * price_per_other)

        # Create and save a new Order instance
        order = Order(
            user=request.user,
            upper_body_clothes=upper_body_clothes,
            lower_body_clothes=lower_body_clothes,
            underwear=underwear,
            other_stuff=other_stuff,
            total_price=total_price
        )
        order.save()

        # Redirect to the order history page
        return redirect('users:ord-history')

    return render(request, 'home.html')  # Handle GET requests if necessary