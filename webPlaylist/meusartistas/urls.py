from django.urls import path
from . import views
from .views import lerartistas, criarartista #atualizarartista, deletarartista

urlpatterns = [
    path('', views.homeartistas, name='homeartistas'),
    path('lerartistas', lerartistas, name='lerartistas'),
    path('criarartista', criarartista, name='criarartista')
    #path('atualizarartista/<int:pk>', atualizarartista, name='atualizarartista'),
    #path('deletarartista/<int:pk>', deletarartista, name='deletarartista')
]