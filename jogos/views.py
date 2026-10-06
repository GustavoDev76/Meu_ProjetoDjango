import json
import urllib.request
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import Jogo, JogoLoja
from .forms import JogoForm, JogoLojaForm, CheckoutForm, CadastroComEmailForm

# --- AUTENTICAÇÃO E REGISTO ---

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CadastroComEmailForm(request.POST)
        if form.is_valid():
            # 1. Salva o usuário no banco de dados com e-mail
            user = form.save()

            # --- INTEGRAÇÃO EMAILJS (Via urllib nativo do Python) ---
            emailjs_url = 'https://api.emailjs.com/api/v1.0/email/send'
            payload = {
                'service_id': 'SEU_SERVICE_ID',
                'template_id': 'SEU_TEMPLATE_ID',
                'user_id': 'SUA_PUBLIC_KEY',
                'accessToken': 'SUA_PRIVATE_KEY',
                'template_params': {
                    'nome_usuario': user.username,
                    'email_destino': user.email
                }
            }

            try:
                # Transforma o payload num JSON em bytes para envio HTTP nativo
                data = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(
                    emailjs_url,
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )

                # Dispara a requisição para o EmailJS
                with urllib.request.urlopen(req, timeout=10) as resposta:
                    if resposta.status != 200:
                        print(f"Erro EmailJS: {resposta.read().decode('utf-8')}")
            except Exception as e:
                print(f"Erro de conexão EmailJS: {e}")
            # --------------------------

            # 2. Faz o login automático e redireciona para a biblioteca
            login(request, user)
            messages.success(request, f'Bem-vindo ao Game Vault, {user.username}!')
            return redirect('home')
    else:
        form = CadastroComEmailForm()

    return render(request, 'registration/register.html', {'form': form})


# --- VIEWS DA BIBLIOTECA PESSOAL ---

def home(request):
    jogos = Jogo.objects.all()
    return render(request, 'home.html', {'jogos': jogos})

def filtrar_status(request, status_nome):
    jogos = Jogo.objects.filter(status=status_nome)
    return render(request, 'home.html', {'jogos': jogos})

def detalhes(request, pk):
    jogo = get_object_or_404(Jogo, pk=pk)
    return render(request, 'detalhes.html', {'jogo': jogo})

def criar_jogo(request):
    if request.method == 'POST':
        form = JogoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = JogoForm()
    return render(request, 'form_jogo.html', {'form': form, 'titulo_pagina': 'Adicionar Jogo'})

def editar_jogo(request, pk):
    jogo = get_object_or_404(Jogo, pk=pk)
    if request.method == 'POST':
        form = JogoForm(request.POST, instance=jogo)
        if form.is_valid():
            form.save()
            return redirect('detalhe_jogo', pk=jogo.pk)
    else:
        form = JogoForm(instance=jogo)
    return render(request, 'form_jogo.html', {'form': form, 'titulo_pagina': 'Editar Jogo'})

def eliminar_jogo(request, pk):
    jogo = get_object_or_404(Jogo, pk=pk)
    if request.method == 'POST':
        jogo.delete()
        return redirect('home')
    return render(request, 'confirmar_eliminar.html', {'jogo': jogo})


# --- VIEWS DA LOJA / STOREFRONT ---

def loja(request):
    ofertas = JogoLoja.objects.all()
    return render(request, 'loja.html', {'ofertas': ofertas})

def criar_jogo_loja(request):
    if request.method == 'POST':
        form = JogoLojaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loja')
    else:
        form = JogoLojaForm()
    return render(request, 'form_jogo.html', {'form': form, 'titulo_pagina': 'Adicionar Jogo à Loja'})

def checkout_jogo(request, pk):
    jogo = get_object_or_404(JogoLoja, pk=pk)
    
    if jogo.eh_gratis and jogo.link_compra_jogar:
        return redirect(jogo.link_compra_jogar)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            return render(request, 'compra_sucesso.html', {
                'jogo': jogo,
                'nome': dados['nome_completo'],
                'email': dados['email'],
                'metodo': dict(form.fields['metodo_pagamento'].choices)[dados['metodo_pagamento']]
            })
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['email'] = request.user.email
            initial_data['nome_completo'] = request.user.get_full_name() or request.user.username
            
        form = CheckoutForm(initial=initial_data)

    return render(request, 'checkout.html', {'jogo': jogo, 'form': form})

def editar_jogo_loja(request, pk):
    jogo = get_object_or_404(JogoLoja, pk=pk)
    if request.method == 'POST':
        form = JogoLojaForm(request.POST, instance=jogo)
        if form.is_valid():
            form.save()
            return redirect('loja')
    else:
        form = JogoLojaForm(instance=jogo)
    return render(request, 'form_jogo.html', {'form': form, 'titulo_pagina': f'Editar {jogo.titulo}'})