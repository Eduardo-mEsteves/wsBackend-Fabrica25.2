from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse
from .models import Musica
from .forms import MusicaForm

# Create your views here.

import requests

def buscarmusicaitunes(titulo, album):
    url = "https://itunes.apple.com/search"
    params = {
        "term": titulo,
        "entity": "song",
        "limit": 20
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for track in data.get('results', []):
            # Verifica se o álbum digitado corresponde exatamente ao digitado
            if track.get('collectionName', '').lower() == album.lower():
                return {
                    'nome': track.get('trackName', ''),
                    'artista': track.get('artistName', ''),
                    'album': track.get('collectionName', ''),
                    'ano': track.get('releaseDate', '')[:4],
                    'capa': track.get('artworkUrl100', '')
                }
    # Nenhum resultado exato encontrado
    return None

def home(request):
    return render(request, 'homeplaylist.html')

def lermusicas(request):
    musicas = Musica.objects.all()
    return render(request, 'lermusicas.html', {'musicas': musicas})

def criarmusica(request):
    if request.method == 'POST':
        form = MusicaForm(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            album = form.cleaned_data['album']
            
            dados = buscarmusicaitunes(titulo, album)

            if dados:
                # Verifica se já existe música com mesmo título e álbum
                existe = Musica.objects.filter(
                    titulo=dados['nome'],
                    album=dados['album']
                ).exists()
                
                if existe:
                    form.add_error('titulo', 'Você já adicionou essa música')
                else:
                    # Salva música no banco
                    Musica.objects.create(
                        titulo=dados['nome'],
                        artista=dados['artista'],
                        album=dados['album'],
                        ano_lancamento=int(dados['ano']) if dados['ano'].isdigit() else 0,
                        capa_url=dados.get('capa', '')
                    )

                    return redirect('lermusicas')
            else:
                # Música não encontrada
                form.add_error('titulo', 'Música não encontrada, tente alguma outra')
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
            titulo = form.cleaned_data['titulo']
            album = form.cleaned_data['album']
            
            # Consulta no iTunes
            dados = buscarmusicaitunes(titulo, album)
            
            if dados:
                # Verifica duplicata ignorando a própria música
                existe = Musica.objects.filter(
                    titulo=dados['nome'],
                    album=dados['album']
                ).exclude(pk=musica.pk).exists()
                
                if existe:
                    form.add_error('titulo', 'Já existe outra música com este título e álbum')
                else:
                    # Atualiza os campos
                    musica.titulo = dados['nome']
                    musica.artista = dados['artista']
                    musica.album = dados['album']
                    musica.ano_lancamento = int(dados['ano']) if dados['ano'].isdigit() else 0
                    musica.capa_url = dados.get('capa', '')
                    musica.save()
                    return redirect('lermusicas')
            else:
                form.add_error('titulo', 'Música não encontrada, tente alguma outra')

              
    else:
        form = MusicaForm(instance=musica)
    return render(request, 'criarmusica.html', {'musica': form})