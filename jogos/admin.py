from django.contrib import admin
from .models import Jogo

@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'plataforma', 'status', 'nota') # Colunas que vão aparecer na lista
    list_filter = ('plataforma', 'status')                   # Filtros laterais
    search_fields = ('titulo', 'plataforma')                 # Barra de pesquisa