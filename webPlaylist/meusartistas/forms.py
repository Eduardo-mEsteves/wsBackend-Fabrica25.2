from django import forms
from .models import Artista

class ArtistaForm(forms.ModelForm):
    class Meta:
        model = Artista
        fields = ['nome', 'nascimento', 'origem', 'estilo']

           