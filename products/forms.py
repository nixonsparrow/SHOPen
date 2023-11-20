from django import forms

from products.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["address"]
