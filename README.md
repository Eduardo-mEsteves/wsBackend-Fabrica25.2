# wsBackend-Fabrica25.2
**Desafio da Fábrica de Software 2025.2**

---

# Biblioteca Musical Django

Este projeto é uma **aplicação Django** para gerenciar **playlists de músicas** e uma **coleção de artistas**.  
Ele integra com a API pública do **iTunes**, permitindo buscar informações reais de músicas e artistas.

---

## Funcionalidades

### Artistas
- Adicionar novos artistas consultando dados reais do iTunes.
- Listar todos os artistas cadastrados.
- Atualizar informações de um artista.
- Deletar artistas.
- Exibe informações como:
  - País de origem
  - Gênero musical
  - Álbum de capa
  - Quantidade de álbuns

### Músicas
- Adicionar músicas a uma playlist consultando dados reais do iTunes.
- Evita duplicatas (mesmo título e álbum).
- Atualizar informações das músicas.
- Deletar músicas.
- Listar todas as músicas da playlist.

---

## Instalação

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd meuprojeto
```

2. Crie um ambiente virtual e ative-o:

```bash
python -m venv venv
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Faça as migrações do banco
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Crie um superuser (opcional)
```bash
python manage.py createsuperuser
```

6. Inicie o servidor
```bash
python manage.py runserver
```

---

## Uso

- Acesse o projeto em: http://127.0.0.1:8000/
- Para acessar a playlist de músicas: http://127.0.0.1:8000/
- Para acessar a coleção de artistas: http://127.0.0.1:8000/artistas/

---

## Integração com o iTunes

# URL	/ Name /	Descrição
/	homeplaylist /	Página inicial da playlist
/lermusicas	/lermusicas	/Lista todas as músicas
/criarmusica/	criarmusica/	Cria uma nova música
/atualizarmusica/int:pk /atualizarmusica	/Atualiza música existente
/deletarmusica/int:pk /deletarmusica	/Deleta música


# URL /	Name / Descrição
/artistas/	homeartistas/	Página inicial dos artistas
/artistas/lerartistas	/lerartistas/	Lista todos os artistas
/artistas/criarartista	/criarartista	/Cria um novo artista
/artistas/atualizarartista/int:pk / atualizarartista	/Atualiza artista existente
/artistas/deletarartista/int:pk / deletarartista/	Deleta artista
/artistas/ver_homeplaylist/	ver_homeplaylist	/ Link para a playlist

---

## Observações sobre API

- A API usada as vezes acaba passando por problemas na hora de encontrar os resultados esperados, entregando resultados não desejados ou simplesmente não entregando. Fora isso, a API está com o devido funcionamento nas aplicações.


---

## Autor 

- Eduardo da Franca Maciel Esteves
