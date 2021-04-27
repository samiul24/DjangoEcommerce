from django import forms
from order.models import ShopCart


class ShopCartForm(forms.ModelForm):
    class Meta:
        model = ShopCart
        fields = ['Quantity',]
