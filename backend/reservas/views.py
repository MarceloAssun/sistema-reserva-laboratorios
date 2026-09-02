from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from contas.grupos import is_administrador, is_professor
from contas.permissions import ReservaPermission
from reservas.models import Reserva, StatusReserva
from reservas.serializers import ReservaSerializer
from reservas.services import ha_conflito


class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaSerializer
    permission_classes = [ReservaPermission]
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        qs = Reserva.objects.select_related("laboratorio", "professor")
        user = self.request.user
        if is_administrador(user):
            qs = qs.all()
        elif is_professor(user):
            qs = qs.filter(professor=user)
        else:
            return Reserva.objects.none()

        status_filtro = self.request.query_params.get("status")
        if status_filtro:
            qs = qs.filter(status=status_filtro)

        laboratorio = self.request.query_params.get("laboratorio")
        if laboratorio:
            qs = qs.filter(laboratorio_id=laboratorio)

        data_inicio = self.request.query_params.get("data_inicio")
        data_fim = self.request.query_params.get("data_fim")
        if data_inicio:
            qs = qs.filter(data__gte=data_inicio)
        if data_fim:
            qs = qs.filter(data__lte=data_fim)

        return qs

    def perform_create(self, serializer):
        serializer.save()

    def _garantir_pendente(self, reserva):
        if reserva.status != StatusReserva.PENDENTE:
            raise ValidationError(
                "Somente solicitações pendentes podem ser aprovadas ou rejeitadas."
            )

    @action(detail=True, methods=["post"])
    def aprovar(self, request, pk=None):
        if not is_administrador(request.user):
            raise PermissionDenied("Somente administradores podem aprovar reservas.")
        reserva = self.get_object()
        self._garantir_pendente(reserva)
        if ha_conflito(
            reserva.laboratorio,
            reserva.data,
            reserva.hora_inicio,
            reserva.hora_fim,
            exclude_id=reserva.id,
        ):
            raise ValidationError(
                "Não é possível aprovar: já existe reserva aprovada com horário sobreposto "
                "para este laboratório."
            )
        reserva.status = StatusReserva.APROVADA
        reserva.save(update_fields=["status"])
        return Response(self.get_serializer(reserva).data)

    @action(detail=True, methods=["post"])
    def rejeitar(self, request, pk=None):
        if not is_administrador(request.user):
            raise PermissionDenied("Somente administradores podem rejeitar reservas.")
        reserva = self.get_object()
        self._garantir_pendente(reserva)
        reserva.status = StatusReserva.REJEITADA
        reserva.save(update_fields=["status"])
        return Response(self.get_serializer(reserva).data)

    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        reserva = self.get_object()
        if reserva.status in (StatusReserva.CANCELADA, StatusReserva.REJEITADA):
            raise ValidationError("Esta reserva não pode ser cancelada.")

        if is_administrador(request.user):
            reserva.status = StatusReserva.CANCELADA
            reserva.save(update_fields=["status"])
            return Response(self.get_serializer(reserva).data)

        if is_professor(request.user) and reserva.professor_id == request.user.id:
            reserva.status = StatusReserva.CANCELADA
            reserva.save(update_fields=["status"])
            return Response(self.get_serializer(reserva).data)

        raise PermissionDenied("Você não pode cancelar esta reserva.")
