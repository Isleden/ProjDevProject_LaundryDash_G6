# forms.py
from django import forms
from .models import Order, UserProfile, Customer, Driver, Business
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['upper_body_clothes', 'lower_body_clothes', 'underwear', 'other_stuff']

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('driver', 'Driver'),
        ('business', 'Business Owner'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)

    # Customer fields
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    phone_number = forms.CharField(required=False, max_length=15)

    # Business fields
    business_name = forms.CharField(required=False, max_length=100)
    business_address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    logo = forms.ImageField(required=False)

    # Driver fields
    vehicle_details = forms.CharField(required=False, max_length=100)
    license_number = forms.CharField(required=False, max_length=50)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')

        if user_type == 'customer':
            if not cleaned_data.get('address'):
                self.add_error('address', 'Address is required for customers.')
            if not cleaned_data.get('phone_number'):
                self.add_error('phone_number', 'Phone number is required for customers.')

        elif user_type == 'business':
            if not cleaned_data.get('business_name'):
                self.add_error('business_name', 'Business name is required.')
            if not cleaned_data.get('business_address'):
                self.add_error('business_address', 'Business address is required.')

        elif user_type == 'driver':
            if not cleaned_data.get('vehicle_details'):
                self.add_error('vehicle_details', 'Vehicle details are required.')
            if not cleaned_data.get('license_number'):
                self.add_error('license_number', 'License number is required.')
                
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create UserProfile with selected user type
            user_profile = UserProfile.objects.create(user=user, user_type=self.cleaned_data['user_type'])
            
            # Create the corresponding model instance based on user type
            if self.cleaned_data['user_type'] == 'customer':
                Customer.objects.create(
                    user_profile=user_profile,
                    address=self.cleaned_data['address'],
                    phone_number=self.cleaned_data['phone_number']
                )

            elif self.cleaned_data['user_type'] == 'driver':
                Driver.objects.create(
                    user_profile=user_profile,
                    vehicle_details=self.cleaned_data['vehicle_details'],
                    license_number=self.cleaned_data['license_number']
                )
                
            elif self.cleaned_data['user_type'] == 'business':
                Business.objects.create(
                    user_profile=user_profile,
                    business_name=self.cleaned_data['business_name'],
                    business_address=self.cleaned_data['business_address'],
                    logo=self.cleaned_data['logo']
                )
        
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['address', 'phone_number']

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['vehicle_details', 'license_number']

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['business_name', 'business_address', 'logo']