from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            try:
                user_role = request.user.userprofile.role
                if user_role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            except AttributeError:
                messages.error(request, 'User profile not found.')
                return redirect('home')
            
            raise PermissionDenied("You don't have permission to access this page.")
        return _wrapped_view
    return decorator

# ============================================================================
# USER MANAGEMENT PERMISSIONS
# ============================================================================

def can_manage_all_profiles(user):
    """Can manage all user profiles (admin only)"""
    return user.userprofile.role == 'admin'

def can_view_all_profiles(user):
    """Can view all user profiles (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

def can_edit_own_profile(user):
    """Can edit their own profile (all authenticated users)"""
    return user.is_authenticated

def can_suspend_users(user):
    """Can suspend user accounts (admin only)"""
    return user.userprofile.role == 'admin'

# ============================================================================
# BOOKING MANAGEMENT PERMISSIONS
# ============================================================================

def can_manage_bookings(user):
    """Can manage all bookings (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

def can_approve_bookings(user):
    """Can approve/reject booking requests (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

def can_view_all_bookings(user):
    """Can view all bookings (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

def can_create_bookings(user):
    """Can create bookings (all authenticated users)"""
    return user.is_authenticated

def can_cancel_own_bookings(user):
    """Can cancel their own bookings (all authenticated users)"""
    return user.is_authenticated

def can_cancel_any_bookings(user):
    """Can cancel any booking (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

# ============================================================================
# RESOURCE MANAGEMENT PERMISSIONS
# ============================================================================

def can_manage_resources(user):
    """Can create, edit, delete resources (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

def can_view_resources(user):
    """Can view resources (all authenticated users)"""
    return user.is_authenticated

def can_set_resource_status(user):
    """Can set resource status (maintenance, available, etc.) (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

def can_assign_resources(user):
    """Can assign resources to users (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

# ============================================================================
# LEASE MANAGEMENT PERMISSIONS
# ============================================================================

def can_manage_leases(user):
    """Can manage all leases (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

def can_approve_leases(user):
    """Can approve/reject lease requests (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

def can_view_all_leases(user):
    """Can view all leases (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

def can_create_lease_requests(user):
    """Can create lease requests (all authenticated users)"""
    return user.is_authenticated

def can_terminate_leases(user):
    """Can terminate leases (admin only)"""
    return user.userprofile.role == 'admin'

# ============================================================================
# SUBSCRIPTION MANAGEMENT PERMISSIONS
# ============================================================================

def can_manage_subscriptions(user):
    """Can manage all subscriptions (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

def can_view_all_subscriptions(user):
    """Can view all subscriptions (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

def can_create_subscriptions(user):
    """Can create subscriptions (all authenticated users)"""
    return user.is_authenticated

def can_cancel_subscriptions(user):
    """Can cancel subscriptions (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

# ============================================================================
# REPORTING AND ANALYTICS PERMISSIONS
# ============================================================================

def can_view_reports(user):
    """Can view reports and analytics (staff and admin)"""
    return user.userprofile.role in ['staff', 'admin']

def can_export_data(user):
    """Can export data and reports (admin only)"""
    return user.userprofile.role == 'admin'

def can_view_financial_reports(user):
    """Can view financial reports (admin only)"""
    return user.userprofile.role == 'admin'

# ============================================================================
# SYSTEM ADMINISTRATION PERMISSIONS
# ============================================================================

def can_manage_system_settings(user):
    """Can manage system settings (admin only)"""
    return user.userprofile.role == 'admin'

def can_manage_membership_plans(user):
    """Can manage membership plans (admin only)"""
    return user.userprofile.role == 'admin'

def can_access_admin_panel(user):
    """Can access Django admin panel (admin only)"""
    return user.userprofile.role == 'admin'

# ============================================================================
# UTILITY PERMISSIONS
# ============================================================================

def is_owner_or_admin(user, obj):
    """Check if user is the owner of an object or is admin"""
    if user.userprofile.role == 'admin':
        return True
    return obj.user == user

def is_owner_or_staff(user, obj):
    """Check if user is the owner of an object or is staff/admin"""
    if user.userprofile.role in ['staff', 'admin']:
        return True
    return obj.user == user

def can_access_dashboard(user):
    """Can access the dashboard (all authenticated users)"""
    return user.is_authenticated

def can_view_own_data(user):
    """Can view their own data (all authenticated users)"""
    return user.is_authenticated
