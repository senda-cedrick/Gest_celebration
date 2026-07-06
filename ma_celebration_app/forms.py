from django import forms
from .models import WeddingCelebration


class WeddingCelebrationForm(forms.ModelForm):
    class Meta:
        model = WeddingCelebration
        fields = [
            'groom_name',
            'bride_name',
            'wedding_date',
            'ceremony_time',
            'church_name',
            'priest_name',
            'notes',
        ]
        labels = {
            'groom_name': 'Nom du marié',
            'bride_name': 'Nom de la mariée',
            'wedding_date': 'Date de la célébration',
            'ceremony_time': 'Heure de la cérémonie',
            'church_name': 'Église / Lieu',
            'priest_name': 'Nom du prêtre',
            'notes': 'Notes / Informations complémentaires',
        }
        widgets = {
            'wedding_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'jj/mm/aaaa'}),
            'ceremony_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'HH:MM'}),
            'groom_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Jean Dupont'}),
            'bride_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Marie Martin'}),
            'church_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Église Saint-Pierre'}),
            'priest_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Révérend Durand'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex: Décoration blanche et fleurs fraîches.'}),
        }
