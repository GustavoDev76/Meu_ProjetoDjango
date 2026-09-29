from django.db import models

class Jogo(models.Model):
    STATUS_CHOICES = [
        ('A Jogar', 'A Jogar'),
        ('Jogando', 'Jogando'),
        ('Concluído', 'Concluído'),
        ('Abandonado', 'Abandonado'),
    ]

    titulo = models.CharField(max_length=100)
    plataforma = models.CharField(max_length=50)
    descricao = models.TextField(blank=True, default='')
    nota = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='A Jogar')
    imagem_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL da Imagem")

    def __str__(self):
        return self.titulo