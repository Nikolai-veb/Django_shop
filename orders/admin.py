from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name',
                    'email', 'adress', 'postal_code',
                    'city', 'paind', 'created', 'update']
    list_filter = ['paind', 'created', 'update', 'city']
    search_fields = ['first_name', 'last_name', 'email', 'city', 'adress', 'postal_code']
    list_editable = ("paind",)
    inlines = [OrderItemInline]
