from django import forms

from cart.models import Orders

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['full_name', 'phone_number', 'address', 'province', 'district', 'shipping_method', 'payment_method']