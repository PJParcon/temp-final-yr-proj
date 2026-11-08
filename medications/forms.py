from django import forms

from .models import Medication


class MedicationEntryForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ('name', 'strength', 'dosage', 'medication_form', 'frequency', 'instructions')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Paracetamol'}),
            'strength': forms.TextInput(attrs={'placeholder': 'e.g. 500 mg'}),
            'dosage': forms.TextInput(attrs={'placeholder': 'e.g. 1 tablet'}),
            'frequency': forms.TextInput(attrs={'placeholder': 'e.g. Once daily'}),
            'instructions': forms.Textarea(attrs={'placeholder': 'Optional notes from prescription', 'rows': 3}),
        }
