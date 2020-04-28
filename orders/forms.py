from django import forms
from .models import *

class CheckoutProductForm(forms.Form):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
