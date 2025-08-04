from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .forms import (
    CustomUserCreationForm, ResourceForm, BookingForm,
    LeaseContractForm, SubscriptionForm
)
from django.contrib.auth.models import User
from .models import (
    UserProfile, Resource, Booking, LeaseContract,
    MembershipPlan, Subscription
)

def home(request):
    resources = Resource.objects.filter(status='available')
    membership_plans = MembershipPlan.objects.filter(is_active=True)
    return render(request, 'core_app/home.html', {
        'resources': resources,
        'membership_plans': membership_plans
    })

@ensure_csrf_cookie
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                role='member'
            )
            messages.success(request, 'Account created successfully. You can now login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core_app/auth/register.html', {'form': form})

# Profile Views
@login_required
def profile_view(request):
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'role': 'member',
            'phone_number': '',
            'address': '',
            'company_name': ''
        }
    )
    
    return render(request, 'core_app/profile/view.html', {
        'profile': profile
    })

@login_required
def profile_edit(request):
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'role': 'member',
            'phone_number': '',
            'address': '',
            'company_name': ''
        }
    )
    
    if request.method == 'POST':
        profile.phone_number = request.POST.get('phone_number', '')
        profile.address = request.POST.get('address', '')
        profile.company_name = request.POST.get('company_name', '')
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    
    return render(request, 'core_app/profile/edit.html')

# Dashboard Views
@login_required
def member_dashboard(request):
    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'role': 'member',
            'phone_number': '',
            'address': '',
            'company_name': ''
        }
    )
    
    if user_profile.role not in ['member', 'staff', 'admin']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get bookings based on user role
    if user_profile.role == 'member':
        bookings = request.user.bookings.all()[:5]
    else:
        # Staff/Admin see all recent bookings
        bookings = Booking.objects.all().order_by('-created_at')[:10]
    
    context = {
        'bookings': bookings,
        'active_subscription': Subscription.objects.filter(
            user=request.user,
            is_active=True,
            end_date__gte=timezone.now().date()
        ).first()
    }
    
    if user_profile.role in ['staff', 'admin']:
        context.update({
            'pending_bookings': Booking.objects.filter(status='pending').count(),
            'active_leases': LeaseContract.objects.filter(status='active').count(),
            'maintenance_resources': Resource.objects.filter(status='maintenance').count(),
        })
    
    return render(request, 'core_app/dashboard.html', context)

# Resource Views
@login_required
def resource_list(request):
    resources = Resource.objects.all()
    resource_type = request.GET.get('type')
    if resource_type:
        resources = resources.filter(type=resource_type)
    
    return render(request, 'core_app/resources/list.html', {'resources': resources})

@login_required
def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    context = {
        'resource': resource,
        'upcoming_bookings': resource.bookings.filter(
            status='approved',
            end_time__gte=timezone.now()
        ).order_by('start_time')[:5]
    }
    return render(request, 'core_app/resources/detail.html', context)

@login_required
def resource_create(request):
    if request.user.userprofile.role not in ['staff', 'admin']:
        messages.error(request, 'Access denied.')
        return redirect('resources')
    
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource created successfully.')
            return redirect('resources')
    else:
        form = ResourceForm()
    
    return render(request, 'core_app/resources/form.html', {'form': form})

# Booking Views
@login_required
def booking_create(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.resource = resource
            booking.save()
            messages.success(request, 'Booking request submitted successfully.')
            return redirect('booking_list')
    else:
        form = BookingForm(initial={'resource': resource})
    
    return render(request, 'core_app/bookings/form.html', {'form': form, 'resource': resource})

@login_required
def booking_list(request):
    user_profile = request.user.userprofile
    if user_profile.role in ['staff', 'admin']:
        bookings = Booking.objects.all()
    else:
        bookings = request.user.bookings.all()
    
    status = request.GET.get('status')
    if status:
        bookings = bookings.filter(status=status)
    
    return render(request, 'core_app/bookings/list.html', {'bookings': bookings})

@login_required
def booking_approve(request, pk):
    if request.user.userprofile.role not in ['staff', 'admin']:
        messages.error(request, 'Access denied.')
        return redirect('bookings')
    
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = 'approved'
    booking.save()
    messages.success(request, 'Booking approved successfully.')
    return redirect('booking_list')

# Subscription Views
@login_required
def subscription_create(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            messages.success(request, 'Subscription created successfully.')
            return redirect('dashboard')
    else:
        form = SubscriptionForm()
    
    return render(request, 'core_app/subscriptions/form.html', {'form': form})

@login_required
def subscription_list(request):
    if request.user.userprofile.role in ['staff', 'admin']:
        subscriptions = Subscription.objects.all()
    else:
        subscriptions = request.user.subscriptions.all()
    
    return render(request, 'core_app/subscriptions/list.html', {'subscriptions': subscriptions})

# Lease Views
@login_required
def lease_create(request, resource_id):
    if request.user.userprofile.role not in ['staff', 'admin']:
        messages.error(request, 'Access denied.')
        return redirect('resources')
    
    resource = get_object_or_404(Resource, pk=resource_id)
    
    if request.method == 'POST':
        form = LeaseContractForm(request.POST)
        if form.is_valid():
            lease = form.save(commit=False)
            lease.user = request.user
            lease.resource = resource
            lease.save()
            messages.success(request, 'Lease contract created successfully.')
            return redirect('lease_list')
    else:
        form = LeaseContractForm(initial={'resource': resource})
    
    return render(request, 'core_app/leases/form.html', {'form': form, 'resource': resource})

@login_required
def lease_list(request):
    if request.user.userprofile.role in ['staff', 'admin']:
        leases = LeaseContract.objects.all()
    else:
        leases = request.user.leases.all()
    
    status = request.GET.get('status')
    if status:
        leases = leases.filter(status=status)
    
    return render(request, 'core_app/leases/list.html', {'leases': leases})

# User Management Views
@login_required
def user_list(request):
    """List all users (staff and admin only)"""
    if request.user.userprofile.role not in ['staff', 'admin']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    users = User.objects.select_related('userprofile').all()
    return render(request, 'core_app/users/list.html', {'users': users})

@login_required
def user_detail(request, user_id):
    """View user details (staff and admin only)"""
    if request.user.userprofile.role not in ['staff', 'admin']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    user = get_object_or_404(User, id=user_id)
    return render(request, 'core_app/users/detail.html', {'target_user': user})
