from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jogo/<int:pk>/', views.detalhe_jogo, name='detalhe_jogo'),
    path('jogo/novo/', views.criar_jogo, name='criar_jogo'),
    path('jogo/<int:pk>/editar/', views.editar_jogo, name='editar_jogo'),
    path('jogo/<int:pk>/eliminar/', views.eliminar_jogo, name='eliminar_jogo'),
]