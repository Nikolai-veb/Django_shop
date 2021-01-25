from django import forms

class CouponApplyForm(forms.Form):
    """Form addly coupon"""
    code = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control input-cart", "id":"inputfname", "placeholder":"Coupon Code" }))

