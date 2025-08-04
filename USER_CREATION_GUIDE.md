# User Creation Guide - Space Flow

This guide shows you how to create users in the Space Flow coworking space management system using different methods.

## 🎯 **Method 1: Django Admin Interface (Recommended)**

### **Step 1: Access Admin Panel**
1. Go to `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials

### **Step 2: Create User**
1. Click on **"Users"** under **"AUTHENTICATION AND AUTHORIZATION"**
2. Click **"Add user"** button
3. Fill in the form:
   - **Username**: `member1`
   - **Password**: `memberpass123`
   - **Password confirmation**: `memberpass123`
4. Click **"Save"**

### **Step 3: Create User Profile**
1. After creating the user, you'll be redirected to the user edit page
2. Scroll down to **"User profiles"** section
3. Click **"Add another User profile"**
4. Fill in:
   - **User**: Select the user you just created
   - **Role**: Choose `member`, `staff`, or `admin`
   - **Phone number**: `+1234567890`
   - **Address**: `123 Main St`
   - **Company name**: `Example Company`
5. Click **"Save"**

## 🖥️ **Method 2: Django Management Command**

### **Step 1: Create User via Command Line**
```bash
# Create a member user
python3 manage.py create_user member1 --role member --first-name "John" --last-name "Doe" --email "john@example.com" --phone "+1234567890" --company "Example Corp"

# Create a staff user
python3 manage.py create_user staff1 --role staff --first-name "Jane" --last-name "Smith" --email "jane@example.com" --phone "+1234567891" --company "Space Flow Staff"

# Create an admin user
python3 manage.py create_user admin2 --role admin --first-name "Admin" --last-name "User" --email "admin2@example.com" --phone "+1234567892" --company "Space Flow Admin"
```

### **Step 2: Interactive Password Entry**
If you don't provide a password, the command will prompt you:
```bash
Enter password: 
Confirm password: 
```

## 🐍 **Method 3: Django Shell**

### **Step 1: Open Django Shell**
```bash
python3 manage.py shell
```

### **Step 2: Create Users Programmatically**
```python
from django.contrib.auth.models import User
from core_app.models import UserProfile

# Create a member user
member_user = User.objects.create_user(
    username='member2',
    email='member2@example.com',
    password='memberpass123',
    first_name='Member',
    last_name='User'
)

# The UserProfile will be created automatically by the signal
# But you can update the role
member_profile = member_user.userprofile
member_profile.role = 'member'
member_profile.phone_number = '+1234567893'
member_profile.company_name = 'Member Company'
member_profile.save()

print(f"Created member user: {member_user.username}")

# Create a staff user
staff_user = User.objects.create_user(
    username='staff2',
    email='staff2@example.com',
    password='staffpass123',
    first_name='Staff',
    last_name='User'
)

staff_profile = staff_user.userprofile
staff_profile.role = 'staff'
staff_profile.phone_number = '+1234567894'
staff_profile.company_name = 'Space Flow Staff'
staff_profile.save()

print(f"Created staff user: {staff_user.username}")
```

## 🌐 **Method 4: User Registration (Public)**

### **Step 1: Public Registration**
1. Go to `http://127.0.0.1:8000/register/`
2. Fill in the registration form:
   - **Username**: `newmember`
   - **Password**: `newpass123`
   - **Password confirmation**: `newpass123`
3. Click **"Register"**

**Note**: Users created through registration are automatically assigned the `member` role.

## 📊 **Method 5: User Management Dashboard**

### **Step 1: Access User Management**
1. Login as staff or admin user
2. Go to Dashboard
3. Click **"User Management"** in Quick Actions

### **Step 2: View All Users**
- See all users in a table format
- View user details, roles, and status
- Access user-specific actions

## 🔐 **User Roles and Permissions**

### **Member (Default Role)**
- Can book resources
- Can manage own profile
- Can view own bookings and subscriptions
- Can create lease requests

### **Staff**
- All member permissions
- Can approve/reject bookings
- Can manage resources
- Can view all users
- Can manage leases

### **Admin**
- All staff permissions
- Can manage all users
- Can access admin panel
- Can manage system settings
- Can view financial reports

## 📋 **User Creation Checklist**

### **Required Information**
- [ ] Username (unique)
- [ ] Password (secure)
- [ ] Email address
- [ ] Role assignment

### **Optional Information**
- [ ] First name
- [ ] Last name
- [ ] Phone number
- [ ] Company name
- [ ] Address
- [ ] Profile picture

### **Post-Creation Steps**
- [ ] Verify user can login
- [ ] Check role permissions work correctly
- [ ] Test dashboard access
- [ ] Verify profile information

## 🚨 **Security Best Practices**

1. **Strong Passwords**: Use complex passwords for all users
2. **Role Assignment**: Assign minimum necessary permissions
3. **Regular Review**: Periodically review user roles and access
4. **Account Status**: Monitor user account status (active/suspended)
5. **Audit Trail**: Keep track of user creation and role changes

## 🔧 **Troubleshooting**

### **Common Issues**

**User Profile Not Created**
- Check if the signal is working properly
- Manually create UserProfile if needed

**Permission Denied Errors**
- Verify user role is correctly assigned
- Check permission decorators in views

**Login Issues**
- Ensure password is correctly set
- Check if user account is active

### **Useful Commands**
```bash
# List all users
python3 manage.py shell -c "from django.contrib.auth.models import User; print([u.username for u in User.objects.all()])"

# Check user roles
python3 manage.py shell -c "from core_app.models import UserProfile; print([f'{u.user.username}: {u.role}' for u in UserProfile.objects.all()])"

# Reset user password
python3 manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='username'); u.set_password('newpassword'); u.save()"
```

## 📞 **Support**

If you encounter issues with user creation:
1. Check the Django admin logs
2. Verify database migrations are applied
3. Test with a simple user creation first
4. Contact system administrator for complex issues 