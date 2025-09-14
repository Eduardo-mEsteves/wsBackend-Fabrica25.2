from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Artista 
from .forms import ArtistaForm
import requests

# Função que renderiza a página principal da playlist
def homeplaylist(request):
    return render(request, 'homeplaylist.html')

# Função que renderiza a página principal dos artistas
def homeartistas(request):
    return render(request, 'homeartistas.html')

# Função que lista todos os artistas cadastrados
def lerartistas(request):
    artistas = Artista.objects.all()  # Pega todos os artistas do banco
    return render(request, 'lerartistas.html', {'artistas': artistas})  # Passa para o template

# Função que cria um novo artista
def criarartista(request):
    if request.method == 'POST':  # Verifica se o formulário foi enviado
        form = ArtistaForm(request.POST)  # Cria o formulário com os dados do POST
        if form.is_valid():  # Verifica se os dados são válidos
            nome_digitado = form.cleaned_data['nome']  # Pega o nome digitado pelo usuário
            url = f"https://itunes.apple.com/search?term={nome_digitado}&entity=musicArtist&limit=10"

            try:
                response = requests.get(url, timeout=5)  # Consulta a API do iTunes
                data = response.json()  # Converte a resposta em JSON

                if data['resultCount'] == 0:  # Nenhum artista encontrado
                    form.add_error('nome', 'Artista/Banda não encontrado no iTunes.')
                    return render(request, 'criarartista.html', {'artista': form})

                # Seleciona o artista exato ou o primeiro resultado
                results = data['results']
                artista_itunes = next(
                    (a for a in results if a['artistName'].lower() == nome_digitado.lower()),
                    results[0]
                )

                artist_id = artista_itunes['artistId']  # Pega o ID do artista

                # Consulta os álbuns do artista
                url_albuns = f"https://itunes.apple.com/lookup?id={artist_id}&entity=album"
                response_albuns = requests.get(url_albuns, timeout=5)
                albuns_data = response_albuns.json()

                # Filtra apenas álbuns oficiais
                albuns_oficiais = [
                    album for album in albuns_data['results'][1:]
                    if album.get('collectionType') == 'Album'
                ]
                album_count = len(albuns_oficiais)  # Conta quantos álbuns oficiais existem

                # Pega informações adicionais
                origem_valor = artista_itunes.get('country', '').strip() or "Não especificado"
                estilo_valor = artista_itunes.get('primaryGenreName', '').strip() or "Não especificado"
                imagem_valor = albuns_oficiais[0].get('artworkUrl100', '') if albuns_oficiais else ''

                # Cria o artista no banco caso não exista duplicata
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

                return redirect('lerartistas')  # Redireciona para a lista de artistas

            except Exception as e:  # Caso ocorra algum erro na API
                form.add_error('nome', f'Erro ao buscar artista: {e}')
                return render(request, 'criarartista.html', {'artista': form})
    else:
        form = ArtistaForm()  # Cria formulário vazio se for GET

    return render(request, 'criarartista.html', {'artista': form})  # Renderiza template


# Função que deleta um artista
def deletarartista(request, pk):
    artista = Artista.objects.get(pk=pk)  # Busca artista pelo ID
    if request.method == 'POST':  # Confirmação de exclusão
        artista.delete()  # Deleta artista
        return redirect('lerartistas')  # Redireciona para lista de artistas
    return render(request, 'deletarartista.html', {'artista': artista})  # Renderiza página de confirmação


# Função que atualiza as informações de um artista
def atualizarartista(request, pk):
    artista = Artista.objects.get(pk=pk)  # Busca artista pelo ID

    if request.method == 'POST':  # Formulário enviado
        form = ArtistaForm(request.POST, instance=artista)  # Preenche formulário com dados existentes
        if form.is_valid():  # Valida dados
            nome_digitado = form.cleaned_data['nome']  # Nome digitado no formulário

            url = f"https://itunes.apple.com/search?term={nome_digitado}&entity=musicArtist&limit=10"
            try:
                response = requests.get(url, timeout=5)  # Consulta API do iTunes
                data = response.json()

                if data['resultCount'] == 0:  # Nenhum resultado
                    form.add_error('nome', 'Artista/Banda não encontrado no iTunes.')
                    return render(request, 'criarartista.html', {'artista': form})

                # Seleciona artista exato ou primeiro
                results = data['results']
                artista_itunes = next(
                    (a for a in results if a['artistName'].lower() == nome_digitado.lower()),
                    results[0]
                )

                artist_id = artista_itunes['artistId']

                # Consulta álbuns do artista
                url_albuns = f"https://itunes.apple.com/lookup?id={artist_id}&entity=album"
                response_albuns = requests.get(url_albuns, timeout=5)
                albuns_data = response_albuns.json()

                # Filtra apenas álbuns oficiais
                albuns_oficiais = [
                    album for album in albuns_data['results'][1:]
                    if album.get('collectionType') == 'Album'
                ]
                album_count = len(albuns_oficiais)
                imagem_valor = albuns_oficiais[0].get('artworkUrl100', '') if albuns_oficiais else ''

                # Atualiza dados do artista no banco
                artista.origem = artista_itunes.get('country', '').strip() or "Não especificado"
                artista.estilo = artista_itunes.get('primaryGenreName', '').strip() or "Não especificado"
                artista.itunes_id = str(artist_id)
                artista.imagem = imagem_valor
                artista.album_count = album_count

                form.save()  # Salva formulário
                artista.save()  # Salva artista atualizado

                return redirect('lerartistas')  # Redireciona para lista de artistas

            except Exception as e:  # Erro na API
                form.add_error('nome', f'Erro ao atualizar artista: {e}')
                return render(request, 'criarartista.html', {'artista': form})
    else:
        form = ArtistaForm(instance=artista)  # Preenche formulário com dados existentes se for GET

    return render(request, 'criarartista.html', {'artista': form})  # Renderiza template
