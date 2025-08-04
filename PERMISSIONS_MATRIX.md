# Space Flow - Permissions Matrix

This document outlines the permissions and access levels for different user roles in the Space Flow coworking space management system.

## User Roles

- **Member**: Basic user with booking and profile management capabilities
- **Staff**: Operational user with booking approval and resource management capabilities
- **Admin**: Full administrative access with system management capabilities

## Permissions Matrix

| Feature/Function | Member | Staff | Admin |
|------------------|--------|-------|-------|
| **Authentication** | | | |
| Register Account | ✅ | ✅ | ✅ |
| Login/Logout | ✅ | ✅ | ✅ |
| **Profile Management** | | | |
| View Own Profile | ✅ | ✅ | ✅ |
| Edit Own Profile | ✅ | ✅ | ✅ |
| View All Profiles | ❌ | ✅ | ✅ |
| Edit All Profiles | ❌ | ❌ | ✅ |
| Suspend Users | ❌ | ❌ | ✅ |
| **Dashboard Access** | | | |
| Access Dashboard | ✅ | ✅ | ✅ |
| View Personal Stats | ✅ | ✅ | ✅ |
| View System Stats | ❌ | ✅ | ✅ |
| **Resource Management** | | | |
| View Resources | ✅ | ✅ | ✅ |
| Book Resources | ✅ | ✅ | ✅ |
| Create Resources | ❌ | ✅ | ✅ |
| Edit Resources | ❌ | ✅ | ✅ |
| Delete Resources | ❌ | ❌ | ✅ |
| Set Resource Status | ❌ | ✅ | ✅ |
| Assign Resources | ❌ | ✅ | ✅ |
| **Booking Management** | | | |
| Create Bookings | ✅ | ✅ | ✅ |
| View Own Bookings | ✅ | ✅ | ✅ |
| View All Bookings | ❌ | ✅ | ✅ |
| Cancel Own Bookings | ✅ | ✅ | ✅ |
| Cancel Any Bookings | ❌ | ✅ | ✅ |
| Approve/Reject Bookings | ❌ | ✅ | ✅ |
| **Lease Management** | | | |
| Create Lease Requests | ✅ | ✅ | ✅ |
| View Own Leases | ✅ | ✅ | ✅ |
| View All Leases | ❌ | ✅ | ✅ |
| Approve/Reject Leases | ❌ | ✅ | ✅ |
| Terminate Leases | ❌ | ❌ | ✅ |
| **Subscription Management** | | | |
| Create Subscriptions | ✅ | ✅ | ✅ |
| View Own Subscriptions | ✅ | ✅ | ✅ |
| View All Subscriptions | ❌ | ✅ | ✅ |
| Cancel Subscriptions | ❌ | ✅ | ✅ |
| Manage Membership Plans | ❌ | ❌ | ✅ |
| **Reporting & Analytics** | | | |
| View Reports | ❌ | ✅ | ✅ |
| Export Data | ❌ | ❌ | ✅ |
| View Financial Reports | ❌ | ❌ | ✅ |
| **System Administration** | | | |
| Access Admin Panel | ❌ | ❌ | ✅ |
| Manage System Settings | ❌ | ❌ | ✅ |
| User Management | ❌ | ❌ | ✅ |

## Detailed Permission Descriptions

### Member Permissions
- **Profile Management**: Can view and edit their own profile information
- **Resource Booking**: Can view available resources and create booking requests
- **Booking Management**: Can view, create, and cancel their own bookings
- **Lease Requests**: Can submit lease requests for long-term office space
- **Subscriptions**: Can purchase and manage their own membership subscriptions

### Staff Permissions
- **All Member Permissions**: Inherits all member capabilities
- **Booking Approval**: Can approve, reject, or modify booking requests
- **Resource Management**: Can create, edit, and manage resource availability
- **User Support**: Can view all user profiles and assist with account issues
- **Operational Reports**: Can access operational reports and analytics
- **Lease Management**: Can approve and manage lease contracts

### Admin Permissions
- **All Staff Permissions**: Inherits all staff capabilities
- **System Administration**: Full access to Django admin panel
- **User Management**: Can suspend, delete, or modify any user account
- **Financial Management**: Access to financial reports and data export
- **System Configuration**: Can modify system settings and membership plans
- **Resource Control**: Can delete resources and manage system-wide settings

## Permission Implementation

### Using Permission Decorators

```python
from core_app.permissions import role_required

@role_required(['staff', 'admin'])
def approve_booking(request, booking_id):
    # Only staff and admin can access this view
    pass

@role_required(['admin'])
def manage_system_settings(request):
    # Only admin can access this view
    pass
```

### Using Permission Functions

```python
from core_app.permissions import can_approve_bookings, can_manage_resources

def some_view(request):
    if can_approve_bookings(request.user):
        # Show booking approval options
        pass
    
    if can_manage_resources(request.user):
        # Show resource management options
        pass
```

### Template-Level Permissions

```django
{% if user.userprofile.role in 'staff,admin' %}
    <!-- Staff/Admin only content -->
    <a href="{% url 'approve_bookings' %}">Approve Bookings</a>
{% endif %}

{% if user.userprofile.role == 'admin' %}
    <!-- Admin only content -->
    <a href="{% url 'system_settings' %}">System Settings</a>
{% endif %}
```

## Security Considerations

1. **Server-Side Validation**: All permissions are validated on the server side
2. **Role-Based Access Control**: Access is controlled through user roles
3. **Object-Level Permissions**: Users can only access their own data unless they have elevated permissions
4. **Audit Trail**: All administrative actions should be logged for security purposes

## Best Practices

1. **Principle of Least Privilege**: Users should have the minimum permissions necessary
2. **Regular Review**: Periodically review and update user roles and permissions
3. **Documentation**: Keep this permissions matrix updated as features are added
4. **Testing**: Test all permission scenarios to ensure proper access control 