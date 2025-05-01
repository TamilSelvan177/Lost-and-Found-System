from django import forms
from .models import FoundItem

class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItem
        fields = ['item_name', 'category', 'description', 'found_date', 'found_location', 'image']
        widgets = {
            'found_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                },
                format='%Y-%m-%d'
            ),
            'found_location': forms.TextInput(
                attrs={
                    'id': 'id_found_location',  # used by map JS
                    'readonly': 'readonly',
                    'class': 'form-control'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['found_date'].input_formats = ['%Y-%m-%d']
