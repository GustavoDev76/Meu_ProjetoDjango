from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jogo/<int:pk>/', views.detalhes, name='detalhe_jogo'),
    path('jogo/novo/', views.criar_jogo, name='criar_jogo'),
    path('jogo/<int:pk>/editar/', views.editar_jogo, name='editar_jogo'),
    path('jogo/<int:pk>/eliminar/', views.eliminar_jogo, name='eliminar_jogo'),
    path('status/<str:status_nome>/', views.filtrar_status, name='filtrar_status'),
    path('loja/', views.loja, name='loja'),
    path('loja/novo/', views.criar_jogo_loja, name='criar_jogo_loja'),
    path('loja/compra/<int:pk>/', views.checkout_jogo, name='checkout_jogo'),
]