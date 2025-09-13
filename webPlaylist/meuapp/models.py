from django.db import models

# Create your models here.
class Musica(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    artista = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    ano_lancamento = models.PositiveIntegerField()
    capa_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.artista} ({self.ano_lancamento})"
    