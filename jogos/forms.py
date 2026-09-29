from django import forms
from .models import Jogo

class JogoForm(forms.ModelForm):
    class Meta:
        model = Jogo
        fields = ['titulo', 'plataforma', 'status', 'nota', 'imagem_url', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Ex: Plants vs. Zombies'}),
            'plataforma': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Ex: PS5, PC'}),
            'status': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'nota': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'min': 0, 'max': 10}),
            'imagem_url': forms.URLInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'https://exemplo.com/imagem.jpg'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3}),
        }