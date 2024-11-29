from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, UserProfile, Business, Order, Customer, BusinessOwner
from .forms import OrderForm, SignupForm, LoginForm, BusinessForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)

            if user_profile.user_type == 'customer':
                return redirect('users:main')  
            elif user_profile.user_type == 'business_owner':
                return redirect('users:business_dashboard')  
            elif user_profile.user_type == 'driver':
                return redirect('users:driver_dashboard') 

        except UserProfile.DoesNotExist:
            # If no UserProfile is found for the authenticated user, handle this case
            return render(request, 'users/index.html')

    else:
        # If the user is not authenticated, render the index page
        return render(request, 'users/index.html')

def about(request):
    return render(request, 'users/about.html')

def services(request):
    return render(request, 'users/services.html')
def home(request):
    businesses = Business.objects.all()  # Adjust the query if needed, e.g., filter based on owner or other criteria
    user_orders = Order.objects.filter(user=request.user).exclude(status='finished').order_by('-order_date')

    return render(request, 'users/home.html', {'businesses': businesses, 'orders': user_orders})

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
        orders = Order.objects.filter(user=request.user, status='finished')  # Filter orders for the logged-in user
    else:
        orders = []  # No orders if the user is not authenticated
    return render(request, 'users/ord-history.html', {'orders': orders})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
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
            if user_profile.user_type == 'business_owner':
                return redirect('users:business_dashboard')
            else:
                return redirect('users:main')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def deliv_history(request):

    return render(request, 'users/driver_DelivHistory.html')

@login_required
def driver_dashboard(request):
    # driver's dashboard
    return render(request, 'users/driver_dashboard.html')

@login_required
def customer_dashboard(request):
    # Placeholder for the customer's dashboard
    return render(request, 'users/ord-history.html')

@login_required
def edit_customer_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    customer = Customer.objects.get(user_profile=user_profile) 
    
    if request.method == 'POST':
        # Update the fields based on form data
        customer.address = request.POST.get('address')
        customer.phone_number = request.POST.get('phone_number')
        customer.save()
        
        return redirect('users:main')  # Redirect to home or success page
    
    return render(request, 'users/editCustomerProfile.html', {'customer': customer})

@login_required
def edit_business_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Use get_object_or_404 to handle missing Business profiles
    business = get_object_or_404(BusinessOwner, user_profile=user_profile)
    
    if request.method == 'POST':
        # Update fields based on form data
        business.owner_name = request.POST.get('owner_name')
        
        if 'logo' in request.FILES:
            business.logo = request.FILES['logo']
        
        business.save()
        
        return redirect('users:business_dashboard')  # Redirect to dashboard or success page
    
    return render(request, 'users/editBusinessProfile.html', {'business': business})


@login_required
def add_business(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            user_profile = UserProfile.objects.get(user=request.user)
            business.business_owner = BusinessOwner.objects.get(user_profile=user_profile)
            business.save()
            return redirect('users:business_dashboard')  # Replace with your business list view or another URL
    else:
        form = BusinessForm()
    return render(request, 'users/add_business.html', {'form': form})

@login_required
def business_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    business_owner = BusinessOwner.objects.get(user_profile=user_profile)
    businesses = Business.objects.filter(business_owner=business_owner)

    # Fetch all orders related to the business (you can filter by business ID if needed)
    orders = Order.objects.filter(ordered_from_business__in=businesses)

    return render(request, 'users/business_dashboard.html', {
        'businesses': businesses,
        'orders': orders,  # Pass orders to the template
    })
@login_required
def delete_business(request, business_id):
    try:
        # Get the business object by its ID and ensure the user is the owner
        business = Business.objects.get(id=business_id)
        business.delete()
        return redirect('users:business_dashboard')  # Redirect back to the business dashboard after deletion
    except Business.DoesNotExist:
        # If business doesn't exist or the user is not the owner, redirect or show an error
        return redirect('users:business_dashboard')  # You can also render a custom error page here

@login_required
def order_submit(request):
    if request.method == 'POST':
        # Extract data from the form
        business_id = request.POST.get('business_id') 
        upper_body_clothes = int(request.POST.get('upper_body_clothes', 0))
        lower_body_clothes = int(request.POST.get('lower_body_clothes', 0))
        underwear = int(request.POST.get('underwear', 0))
        other_stuff = int(request.POST.get('other_stuff', 0))

        # Fetch the Business instance
        business = get_object_or_404(Business, id=business_id)

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
            ordered_from_business=business,
            upper_body_clothes=upper_body_clothes,
            lower_body_clothes=lower_body_clothes,
            underwear=underwear,
            other_stuff=other_stuff,
            total_price=total_price
        )
        order.save()

        # Redirect to the order history page
        return redirect('users:main')

    return render(request, 'home.html')  # Handle GET requests if necessary

@login_required
def customer_dashboard(request):
    current_order = Order.objects.filter(user=request.user, status__in=['looking_for_driver', 'driver_on_the_way_to_pickup', 'driver_on_the_way_to_laundry', 'laundry_received', 'laundry_cleaning', 'driver_on_the_way_to_customer']).first()
    
    return render(request, 'users/customer_dashboard.html', {
        'current_order': current_order,
    })

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Business logic to update the order status
    if order.status == 'looking_for_driver':
        order.status = 'driver_on_the_way_to_pickup'
    elif order.status == 'driver_on_the_way_to_pickup':
        order.status = 'driver_on_the_way_to_laundry'
    elif order.status == 'driver_on_the_way_to_laundry':
        order.status = 'laundry_received'
    elif order.status == 'laundry_received':
        order.status = 'laundry_cleaning'
    elif order.status == 'laundry_cleaning':
        order.status = 'driver_on_the_way_to_customer'
    elif order.status == 'driver_on_the_way_to_customer':
        order.status = 'delivered'
    elif order.status == 'delivered':
        order.status = 'finished'

    order.save()
    return redirect('users:business_dashboard')  # Redirect to business dashboard after updating the status