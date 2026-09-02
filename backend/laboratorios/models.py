from django.db import models


class Laboratorio(models.Model):
    nome = models.CharField(max_length=100)
    capacidade = models.PositiveIntegerField()
    bloco = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Laboratório"
        verbose_name_plural = "Laboratórios"

    def __str__(self):
        return self.nome
