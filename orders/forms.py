from django import forms
from .models import Order


class OrderCreatedForm(forms.ModelForm):
    """Форма заказов"""
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'postal_code']
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control border"}),
            "last_name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "address": forms.TextInput(attrs={"class": "form-control border"}),
            "city": forms.TextInput(attrs={"class": "form-control border"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control border"}),
        }