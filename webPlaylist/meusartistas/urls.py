from django.urls import path
from . import views
from .views import lerartistas, criarartista, deletarartista #atualizarartista

urlpatterns = [
    path('', views.homeartistas, name='homeartistas'),
    path('lerartistas', lerartistas, name='lerartistas'),
    path('criarartista', criarartista, name='criarartista'),
    path('deletarartista/<int:pk>', deletarartista, name='deletarartista')
    #path('atualizarartista/<int:pk>', atualizarartista, name='atualizarartista')
]