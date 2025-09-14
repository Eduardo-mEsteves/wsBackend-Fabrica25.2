from django.db import models

# Create your models here.
class Artista(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    itunes_id = models.CharField(max_length=36, blank=True, null=True)
    origem = models.CharField(blank=True, null=True)
    estilo = models.CharField(max_length=100)
    imagem = models.URLField(blank=True, null=True)
    album_count = models.PositiveIntegerField(blank=True, null=True)
    def __str__(self):
        return self.nome