from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Artista 
from .forms import ArtistaForm
import requests

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
            nome_digitado = form.cleaned_data['nome']
            url = f"https://itunes.apple.com/search?term={nome_digitado}&entity=musicArtist&limit=10"

            try:
                response = requests.get(url, timeout=5)
                data = response.json()
                if data['resultCount'] == 0:
                    form.add_error('nome', 'Artista/Banda não encontrado no iTunes.')
                    return render(request, 'criarartista.html', {'artista': form})

                results = data['results']
                artista_itunes = next(
                    (a for a in results if a['artistName'].lower() == nome_digitado.lower()),
                    results[0]
                )

                artist_id = artista_itunes['artistId']

                url_albuns = f"https://itunes.apple.com/lookup?id={artist_id}&entity=album"
                response_albuns = requests.get(url_albuns, timeout=5)
                albuns_data = response_albuns.json()

                albuns_oficiais = [
                    album for album in albuns_data['results'][1:]
                    if album.get('collectionType') == 'Album'
                ]
                album_count = len(albuns_oficiais)

                origem_valor = artista_itunes.get('country', '').strip() or "Não especificado"
                estilo_valor = artista_itunes.get('primaryGenreName', '').strip() or "Não especificado"

                imagem_valor = albuns_oficiais[0].get('artworkUrl100', '') if albuns_oficiais else ''

                artista, criado = Artista.objects.get_or_create(
                    nome=artista_itunes.get('artistName'),
                    defaults={
                        'origem': origem_valor,
                        'estilo': estilo_valor,
                        'itunes_id': str(artist_id),
                        'imagem': imagem_valor,
                        'album_count': album_count
                    }
                )

                return redirect('lerartistas')

            except Exception as e:
                form.add_error('nome', f'Erro ao buscar artista: {e}')
                return render(request, 'criarartista.html', {'artista': form})
    else:
        form = ArtistaForm()
    return render(request, 'criarartista.html', {'artista': form})

def deletarartista(request, pk):
    artista = Artista.objects.get(pk=pk)
    if request.method == 'POST':
        artista.delete()
        return redirect('lerartistas')
    return render(request, 'deletarartista.html', {'artista': artista})

def atualizarartista(request, pk):
    artista = Artista.objects.get(pk=pk)

    if request.method == 'POST':
        form = ArtistaForm(request.POST, instance=artista)
        if form.is_valid():
            nome_digitado = form.cleaned_data['nome']

            url = f"https://itunes.apple.com/search?term={nome_digitado}&entity=musicArtist&limit=10"
            try:
                response = requests.get(url, timeout=5)
                data = response.json()

                if data['resultCount'] == 0:
                    form.add_error('nome', 'Artista/Banda não encontrado no iTunes.')
                    return render(request, 'criarartista.html', {'artista': form})

                results = data['results']
                artista_itunes = next(
                    (a for a in results if a['artistName'].lower() == nome_digitado.lower()),
                    results[0]
                )

                artist_id = artista_itunes['artistId']

                url_albuns = f"https://itunes.apple.com/lookup?id={artist_id}&entity=album"
                response_albuns = requests.get(url_albuns, timeout=5)
                albuns_data = response_albuns.json()
                albuns_oficiais = [
                    album for album in albuns_data['results'][1:]
                    if album.get('collectionType') == 'Album'
                ]
                album_count = len(albuns_oficiais)
                imagem_valor = albuns_oficiais[0].get('artworkUrl100', '') if albuns_oficiais else ''

                artista.origem = artista_itunes.get('country', '').strip() or "Não especificado"
                artista.estilo = artista_itunes.get('primaryGenreName', '').strip() or "Não especificado"
                artista.itunes_id = str(artist_id)
                artista.imagem = imagem_valor
                artista.album_count = album_count

                form.save()
                artista.save()

                return redirect('lerartistas')

            except Exception as e:
                form.add_error('nome', f'Erro ao atualizar artista: {e}')
                return render(request, 'criarartista.html', {'artista': form})
    else:
        form = ArtistaForm(instance=artista)
    return render(request, 'criarartista.html', {'artista': form})