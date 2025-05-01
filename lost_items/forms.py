from django import forms
from .models import LostItem

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['item_name', 'category', 'description', 'lost_date', 'lost_location', 'image']
