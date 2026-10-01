# jogos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Jogo
from .forms import JogoForm

# 1. READ (Listagem): Busca TODOS os jogos no banco e envia para a home.html
def home(request):
    jogos = Jogo.objects.all()  # Consulta SQL: SELECT * FROM jogos_jogo;
    return render(request, 'home.html', {'jogos': jogos})

# 2. READ (Detalhes): Busca UM jogo pelo seu ID (pk). Se não achar, dá erro 404.
def detalhe_jogo(request, pk):
    jogo = get_object_or_404(Jogo, pk=pk)
    return render(request, 'detalhes.html', {'jogo': jogo})

# 3. CREATE: Processa o formulário de criação. 
# Exige que o utilizador esteja autenticado (@login_required).
@login_required
def criar_jogo(request):
    # Se o utilizador enviou o formulário (POST), recebe os dados; senão (GET), abre vazio.
    form = JogoForm(request.POST or None)
    if form.is_valid():
        form.save()  # Salva direto no banco de dados
        return redirect('home')  # Redireciona para a página principal
    return render(request, 'form_jogo.html', {'form': form, 'titulo_pagina': 'Adicionar Jogo'})

# 4. UPDATE: Carrega os dados de um jogo existente (instance=jogo) para edição.
@login_required
def editar_jogo(request, pk):
    jogo = get_object_or_404(Jogo, pk=pk)
    form = JogoForm(request.POST or None, instance=jogo)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'form_jogo.html', {'form': form, 'titulo_pagina': 'Editar Jogo'})

# 5. DELETE: Apaga o jogo do banco após o utilizador confirmar via POST.
@login_required
def eliminar_jogo(request, pk):
    jogo = get_object_or_404(Jogo, pk=pk)
    if request.method == 'POST':
        jogo.delete()  # Deleta o registo
        return redirect('home')
    return render(request, 'confirmar_eliminar.html', {'jogo': jogo})

def detalhe_jogo(request, pk):
    # 1. Busca o jogo pelo ID (pk). Se não encontrar, retorna erro 404 (Página não encontrada).
    jogo = get_object_or_404(Jogo, pk=pk)
    
    # 2. Renderiza o HTML passando o objeto do jogo encontrado.
    return render(request, 'detalhes.html', {'jogo': jogo})

def filtrar_status(request, status_nome):
    # 1. Filtra a lista de jogos onde a coluna 'status' bate com a string enviada na URL.
    jogos = Jogo.objects.filter(status__iexact=status_nome)
    
    # 2. Reaproveita a página inicial (home.html), mas exibindo apenas os jogos filtrados.
    return render(request, 'home.html', {
        'jogos': jogos, 
        'status_atual': status_nome
    })