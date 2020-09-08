from django import forms
from .models import Order


class OrderCraeteForm(forms.ModelForm):
    """Форма заказов"""
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'adress', 'city', 'postal_code']
