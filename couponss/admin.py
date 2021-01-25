from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'coupon_start', 'coupon_finish', 'discount', 'active']
    list_filter = ['active', 'coupon_start', 'coupon_finish']
    search_fields = ['code']
    list_editable = ['active']
