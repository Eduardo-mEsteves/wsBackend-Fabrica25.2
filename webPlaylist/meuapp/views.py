from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Musica
from .forms import MusicaForm

# Create your views here.
def home(request):
    return render(request, 'homeplaylist.html')

def lermusicas(request):
    musicas = Musica.objects.all()
    return render(request, 'lermusicas.html', {'musicas': musicas})

def criarmusica(request):
    if request.method == 'POST':
        form = MusicaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lermusicas')
    else:
        form = MusicaForm()
    return render(request, 'criarmusica.html', {'musica': form})
        
def deletarmusica(request, pk):
    musica = Musica.objects.get(pk=pk)
    if request.method == 'POST':
        musica.delete()
        return redirect('lermusicas')
    return render(request, 'deletarmusica.html', {'musica': musica})

def atualizarmusica(request, pk):
    musica = Musica.objects.get(pk=pk)
    if request.method == 'POST':
        form = MusicaForm(request.POST, instance=musica)
        if form.is_valid():
            form.save()
            return redirect('lermusicas')
    else:
        form = MusicaForm(instance=musica)
    return render(request, 'criarmusica.html', {'musica': form})