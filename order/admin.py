from django.contrib import admin
from .models import Order, OrderItem, Coupon


# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_paid', 'first_name', 'email', 'phone_number', 'state', 'city', 'zip_code']
    search_fields = ['user', 'first_name', 'state', 'city']
    inlines = [OrderItemInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'active', 'valid_from', 'valid_to', 'discount',)
