from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from laboratorios.models import Laboratorio


class StatusReserva(models.TextChoices):
    PENDENTE = "PENDENTE", "Pendente"
    APROVADA = "APROVADA", "Aprovada"
    REJEITADA = "REJEITADA", "Rejeitada"
    CANCELADA = "CANCELADA", "Cancelada"


class Reserva(models.Model):
    laboratorio = models.ForeignKey(
        Laboratorio,
        on_delete=models.PROTECT,
        related_name="reservas",
    )
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reservas",
    )
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=StatusReserva.choices,
        default=StatusReserva.PENDENTE,
    )
    observacao = models.TextField(blank=True)
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_solicitacao"]
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        return (
            f"Reserva {self.id} - {self.laboratorio.nome} - "
            f"{self.data} {self.hora_inicio}-{self.hora_fim}"
        )

    def clean(self):
        if self.hora_inicio and self.hora_fim and self.hora_fim <= self.hora_inicio:
            raise ValidationError(
                {"hora_fim": "A hora de término deve ser posterior à hora de início."}
            )
        if self.laboratorio_id and not self.laboratorio.ativo:
            raise ValidationError(
                {"laboratorio": "Não é possível reservar um laboratório inativo."}
            )
