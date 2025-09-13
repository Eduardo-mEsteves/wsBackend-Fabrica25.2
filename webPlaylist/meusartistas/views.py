from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Artista 
from .forms import ArtistaForm

# Create your views here.
def homeartistas(request):
    return render(request, 'homeartistas.html')

def lerartistas(request):
    artistas = Artista.objects.all()
    return render(request, 'lerartistas.html', {'artistas': artistas})

def criarartista(request):
    if request.method == 'POST':
        form = ArtistaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lerartistas')
    else:
        form = ArtistaForm()
    return render(request, 'criarartista.html', {'artista': form})

def deletarartista(request, pk):
    artista = Artista.objects.get(pk=pk)
    if request.method == 'POST':
        artista.delete()
        return redirect('lerartistas')
    return render(request, 'deletarartista.html', {'artista': artista})