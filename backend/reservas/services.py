from reservas.models import Reserva, StatusReserva


def reservas_aprovadas_conflitantes(
    laboratorio, data, hora_inicio, hora_fim, exclude_id=None
):
    qs = Reserva.objects.filter(
        laboratorio=laboratorio,
        data=data,
        status=StatusReserva.APROVADA,
        hora_inicio__lt=hora_fim,
        hora_fim__gt=hora_inicio,
    )
    if exclude_id:
        qs = qs.exclude(pk=exclude_id)
    return qs


def ha_conflito(laboratorio, data, hora_inicio, hora_fim, exclude_id=None):
    return reservas_aprovadas_conflitantes(
        laboratorio, data, hora_inicio, hora_fim, exclude_id
    ).exists()
