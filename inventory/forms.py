from django import forms
from .models import Ingredient, MenuItem, Purchase

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'qty', 'unit', 'unit_price'] 


class MenuForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'image']


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['menu_item']