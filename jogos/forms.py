from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Jogo, JogoLoja


# --- FORMULÁRIO DE CADASTRO COM EMAIL ---
class CadastroComEmailForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'class': 'form-control bg-dark text-white border-secondary',
            'placeholder': 'seu@email.com'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


# --- FORMULÁRIOS DE JOGOS E LOJA ---
class JogoForm(forms.ModelForm):
    class Meta:
        model = Jogo
        fields = ['titulo', 'plataforma', 'status', 'nota', 'imagem_url', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Ex: Plants vs. Zombies'}),
            'plataforma': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'status': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'nota': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'min': 0, 'max': 10}),
            'imagem_url': forms.URLInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'https://exemplo.com/imagem.jpg'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3}),
        }


class JogoLojaForm(forms.ModelForm):
    class Meta:
        model = JogoLoja
        fields = ['titulo', 'plataforma', 'preco', 'eh_gratis', 'link_compra_jogar', 'imagem_url', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Ex: Roblox / FNF'}),
            'plataforma': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'step': '0.01', 'placeholder': '0.00'}),
            'eh_gratis': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'link_compra_jogar': forms.URLInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'https://roblox.com'}),
            'imagem_url': forms.URLInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'https://exemplo.com/capa.jpg'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3}),
        }


class CheckoutForm(forms.Form):
    METODOS_PAGAMENTO = [
        ('pix', '⚡ Pix (Aprovação Instantânea)'),
        ('cartao', '💳 Cartão de Crédito'),
        ('boleto', '📄 Boleto Bancário'),
    ]

    nome_completo = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'O teu nome completo'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'seu@email.com'})
    )
    metodo_pagamento = forms.ChoiceField(
        choices=METODOS_PAGAMENTO,
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'})
    )