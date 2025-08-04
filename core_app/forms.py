from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Resource, Booking, LeaseContract, MembershipPlan, Subscription
from django.utils import timezone

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm',
            'placeholder': 'Username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'type', 'description', 'capacity', 'location', 
                 'amenities', 'price_per_hour', 'monthly_price', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'amenities': forms.Textarea(attrs={'rows': 3}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['resource', 'start_time', 'end_time', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        resource = cleaned_data.get('resource')

        if start_time and end_time:
            if start_time < timezone.now():
                raise forms.ValidationError("Start time cannot be in the past")
            if end_time <= start_time:
                raise forms.ValidationError("End time must be after start time")
            
            # Check for booking conflicts
            if resource:
                conflicts = Booking.objects.filter(
                    resource=resource,
                    status='approved',
                    start_time__lt=end_time,
                    end_time__gt=start_time
                )
                if conflicts.exists():
                    raise forms.ValidationError("This time slot is already booked")

class LeaseContractForm(forms.ModelForm):
    class Meta:
        model = LeaseContract
        fields = ['resource', 'start_date', 'end_date', 'monthly_rent', 
                 'deposit_amount', 'terms_and_conditions']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'terms_and_conditions': forms.Textarea(attrs={'rows': 5}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        resource = cleaned_data.get('resource')

        if start_date and end_date:
            if start_date < timezone.now().date():
                raise forms.ValidationError("Start date cannot be in the past")
            if end_date <= start_date:
                raise forms.ValidationError("End date must be after start date")
            
            # Check for lease conflicts
            if resource:
                conflicts = LeaseContract.objects.filter(
                    resource=resource,
                    status='active',
                    start_date__lt=end_date,
                    end_date__gt=start_date
                )
                if conflicts.exists():
                    raise forms.ValidationError("This resource is already leased for the selected period")

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['plan', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date < timezone.now().date():
                raise forms.ValidationError("Start date cannot be in the past")
            if end_date <= start_date:
                raise forms.ValidationError("End date must be after start date")
