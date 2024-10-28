from django.shortcuts import render, redirect 
from .models import Order
from .forms import OrderForm,SignupForm, LoginForm
from django.contrib.auth import login, authenticate

def index(request):
    return render(request, 'users/index.html')

def about(request):
    return render(request, 'users/about.html')

def home(request):  # Renamed from 'order' to 'home'

    return render(request, 'users/home.html')

def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()  # Save the order
            return redirect('users:home')  # Redirect to home or another page
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
            return redirect('users:main')
    else:
        form = SignupForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users:main')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

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
            user=request.user,  # Make sure to assign the current user
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
