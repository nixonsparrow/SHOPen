from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from products.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["address"]


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
