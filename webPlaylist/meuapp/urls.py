from django.urls import path
from . import views
from .views import lermusicas, criarmusica, atualizarmusica, deletarmusica 

urlpatterns = [
    path('', views.home, name='homeplaylist'),
    path('lermusicas', lermusicas, name='lermusicas'),
    path('criarmusica', criarmusica, name='criarmusica'),
    path('atualizarmusica/<int:pk>', atualizarmusica, name='atualizarmusica'),
    path('deletarmusica/<int:pk>', deletarmusica, name='deletarmusica'),
]