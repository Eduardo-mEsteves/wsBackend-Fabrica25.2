from django.urls import path
from . import views
from .views import lermusicas, criarmusica, atualizarmusica, deletarmusica 

urlpatterns = [
    path('', views.home, name='homeplaylist'),
    path('lermusicas', lermusicas, name='lermusicas'),
    path('criarmusica', criarmusica, name='criarmusica'),
    path('atualizarmusica', atualizarmusica, name='atualizarmusica'),
    path('deletarmusica', deletarmusica, name='deletarmusica'),
]