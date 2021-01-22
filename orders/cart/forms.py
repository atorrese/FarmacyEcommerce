from django import forms
from django.utils.translation import  gettext_lazy as _

from cart.models import Cart

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.CharField(widget=forms.NumberInput(attrs={'class':'size8 m-text18 t-center num-product','value':'1'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class CartAdd(forms.ModelForm):
    update  = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    class Meta:
        model= Cart
        fields = ['quantity','update']
        widgets = {
            'quantity':forms.NumberInput(attrs={'class':'size8 m-text18 t-center num-product','value':'1'}),
            'update':forms.HiddenInput,
        }