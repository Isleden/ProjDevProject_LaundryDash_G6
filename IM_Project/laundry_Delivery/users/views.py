from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, UserProfile, Business, Order, Customer, BusinessOwner, Service, Driver
from .forms import OrderForm, SignupForm, LoginForm, BusinessForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
import json

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

def get_services(request):
    business_id = request.GET.get('business_id')
    services = Service.objects.filter(business=business_id).values(
        'id', 
        'service_name', 
        'description', 
        'light_tendency_price', 
        'light_tendency_minimum',
        'light_tendency_maximum',
        'medium_tendency_price', 
        'medium_tendency_minimum',
        'medium_tendency_maximum',
        'heavy_tendency_price',
        'heavy_tendency_minimum',
        'heavy_tendency_maximum',
    )
    return JsonResponse({'services': list(services)})

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
    orders = Order.objects.filter(status__in=['finished'])
    user_profile = UserProfile.objects.get(user=request.user)
    driver = Driver.objects.get(user_profile=user_profile) 
    accepted_orders = Order.objects.filter(driver=driver)

    return render(request, 'users/driver_DelivHistory.html', {
        'orders': orders,
    })

@login_required
def driver_dashboard(request):
    # driver's dashboard
    orders = Order.objects.filter(status__in=['looking_for_driver'])
    user_profile = UserProfile.objects.get(user=request.user)
    driver = Driver.objects.get(user_profile=user_profile) 
    accepted_orders = Order.objects.filter(driver=driver).exclude(status='finished')
    
    return render(request, 'users/driver_dashboard.html', {
        'orders': orders,
        'accepted_orders': accepted_orders
    })

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
            # Save the business
            business = form.save(commit=False)
            user_profile = UserProfile.objects.get(user=request.user)
            business.business_owner = BusinessOwner.objects.get(user_profile=user_profile)
            business.save()

            # Get services data from the POST request
            services_data = request.POST.get('services')
            if services_data:
                services = json.loads(services_data)  # Convert the JSON string into a Python object
                
                for service_data in services:
                    # Create a new service and associate it with the business
                    Service.objects.create(
                        business=business,
                        service_name=service_data['service_name'],
                        description=service_data['description'],
                        light_tendency_price=service_data['light_tendency_price'],
                        light_tendency_minimum=service_data['light_tendency_minimum'],
                        light_tendency_maximum=service_data['light_tendency_maximum'],
                        medium_tendency_price=service_data['medium_tendency_price'],
                        medium_tendency_minimum=service_data['medium_tendency_minimum'],
                        medium_tendency_maximum=service_data['medium_tendency_maximum'],
                        heavy_tendency_price=service_data['heavy_tendency_price'],
                        heavy_tendency_minimum=service_data['heavy_tendency_minimum'],
                        heavy_tendency_maximum=service_data['heavy_tendency_maximum'],
                    )
            print("Redirecting to business_dashboard")
            return JsonResponse({'success': True, 'redirect_url': reverse('users:business_dashboard')})
        else:
            # If the form is not valid, you may want to handle the errors
            return render(request, 'users/add_business.html', {'form': form, 'error': 'Form is invalid.'})

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
def get_business_details(request, business_id):
    # Fetch the business object using the provided business_id
    print("hey")
    business = get_object_or_404(Business, id=business_id)

    # Serialize the business details along with related data (like services and owner)
    business_data = {
        'business_name': business.business_name,
        'business_address': business.business_address,
        'business_owner': {
            'owner_name': business.business_owner.owner_name,  # Now using the 'owner_name' from BusinessOwner
        },
        'services': [
            {
                'service_name': service.service_name,
                'description': service.description,
                'light_tendency_price': service.light_tendency_price,
                'medium_tendency_price': service.medium_tendency_price,
                'heavy_tendency_price': service.heavy_tendency_price,
            }
            for service in business.service_business.all()  # 'service_business' is the related name for services in Business model
        ]
    }

    # Return the business data as a JSON response
    return JsonResponse(business_data)

    
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
        service_id = request.POST.get('service_id') 
        upper_body_clothes = int(request.POST.get('upper_body_clothes', 0))
        lower_body_clothes = int(request.POST.get('lower_body_clothes', 0))
        underwear = int(request.POST.get('underwear', 0))
        other_stuff = int(request.POST.get('other_stuff', 0))
        total_price = float(request.POST.get('total_price', 0))

        # Fetch the Business instance
        business = get_object_or_404(Business, id=business_id)

        service = get_object_or_404(Service, id=service_id)

        # Create and save a new Order instance
        order = Order(
            user=request.user,
            ordered_from_business=business,
            service=service,
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
def add_service(request):
    if request.method == 'POST':
        business_id = request.POST.get('business_id')
        service_name = request.POST.get('service_name')
        description = request.POST.get('description')

        light_price = request.POST.get('light_tendency_price')
        light_min = request.POST.get('light_tendency_minimum')
        light_max = request.POST.get('light_tendency_maximum')

        medium_price = request.POST.get('medium_tendency_price')
        medium_min = request.POST.get('medium_tendency_minimum')
        medium_max = request.POST.get('medium_tendency_maximum')

        heavy_price = request.POST.get('heavy_tendency_price')
        heavy_min = request.POST.get('heavy_tendency_minimum')
        heavy_max = request.POST.get('heavy_tendency_maximum')

        # Fetch the business
        try:
            business = Business.objects.get(id=business_id)
        except Business.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid business ID'})

        # Create the Service
        service = Service.objects.create(
            business=business,
            service_name=service_name,
            description=description,
            light_tendency_price=light_price,
            light_tendency_minimum=light_min,
            light_tendency_maximum=light_max,
            medium_tendency_price=medium_price,
            medium_tendency_minimum=medium_min,
            medium_tendency_maximum=medium_max,
            heavy_tendency_price=heavy_price,
            heavy_tendency_minimum=heavy_min,
            heavy_tendency_maximum=heavy_max,
        )

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def customer_dashboard(request):
    current_order = Order.objects.filter(user=request.user, status__in=['looking_for_driver', 'driver_on_the_way_to_pickup', 'driver_on_the_way_to_laundry', 'laundry_received', 'laundry_cleaning', 'driver_on_the_way_to_customer']).first()
    
    return render(request, 'users/customer_dashboard.html', {
        'current_order': current_order,
    })

@login_required
def accept_order_driver(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    user_profile = UserProfile.objects.get(user=request.user)
    driver = Driver.objects.get(user_profile=user_profile)

    order.driver = driver
    order.status = 'driver_on_the_way_to_pickup'

    order.save()
    return redirect('users:driver_dashboard')



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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to business dashboard after updating the status