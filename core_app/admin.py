from django.contrib import admin
from .models import UserProfile, MembershipPlan, Resource, Booking, LeaseContract, Subscription

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'account_status', 'company_name')
    list_filter = ('role', 'account_status')
    search_fields = ('user__username', 'company_name')

@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'access_level', 'is_active')
    list_filter = ('is_active', 'access_level')
    search_fields = ('name',)

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'capacity', 'status', 'location')
    list_filter = ('type', 'status')
    search_fields = ('name', 'location')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'resource__type')
    search_fields = ('user__username', 'resource__name')

@admin.register(LeaseContract)
class LeaseContractAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'start_date', 'end_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'resource__name')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'plan')
    search_fields = ('user__username', 'plan__name')


