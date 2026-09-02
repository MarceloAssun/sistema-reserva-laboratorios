from datetime import datetime, timedelta

from rest_framework import serializers

from laboratorios.models import Laboratorio
from reservas.models import Reserva, StatusReserva


class LaboratorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratorio
        fields = ("id", "nome", "capacidade", "bloco", "ativo")


def montar_grade(laboratorio, data):
    ocupados = list(
        Reserva.objects.filter(
            laboratorio=laboratorio,
            data=data,
            status=StatusReserva.APROVADA,
        ).values("id", "hora_inicio", "hora_fim")
    )

    slots = []
    atual = datetime.combine(data, datetime.strptime("07:00", "%H:%M").time())
    fim_expediente = datetime.combine(data, datetime.strptime("22:00", "%H:%M").time())
    while atual < fim_expediente:
        slot_fim = atual + timedelta(hours=1)
        hora_ini = atual.time()
        hora_fim = slot_fim.time()
        conflito = any(
            hora_ini < item["hora_fim"] and hora_fim > item["hora_inicio"]
            for item in ocupados
        )
        slots.append(
            {
                "hora_inicio": hora_ini.strftime("%H:%M"),
                "hora_fim": hora_fim.strftime("%H:%M"),
                "ocupado": conflito,
            }
        )
        atual = slot_fim

    return {
        "laboratorio": laboratorio.id,
        "laboratorio_nome": laboratorio.nome,
        "data": data.isoformat(),
        "reservas_aprovadas": [
            {
                "id": item["id"],
                "hora_inicio": item["hora_inicio"].strftime("%H:%M"),
                "hora_fim": item["hora_fim"].strftime("%H:%M"),
            }
            for item in ocupados
        ],
        "grade": slots,
    }
