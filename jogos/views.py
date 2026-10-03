from django.shortcuts import render, get_object_or_404, redirect
from .models import Jogo, JogoLoja
from .forms import JogoForm, JogoLojaForm, CheckoutForm

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
    
    # Se o jogo for grátis e tiver link direto, redireciona para jogar
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