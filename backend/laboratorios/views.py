from datetime import date

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from contas.permissions import LaboratorioPermission
from laboratorios.models import Laboratorio
from laboratorios.serializers import LaboratorioSerializer, montar_grade


class LaboratorioViewSet(viewsets.ModelViewSet):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer
    permission_classes = [LaboratorioPermission]
    http_method_names = ["get", "post", "put", "patch", "head", "options"]

    @action(detail=True, methods=["get"])
    def disponibilidade(self, request, pk=None):
        laboratorio = self.get_object()
        data_str = request.query_params.get("data")
        if not data_str:
            raise ValidationError({"data": "Informe a data no formato YYYY-MM-DD."})
        try:
            data = date.fromisoformat(data_str)
        except ValueError as exc:
            raise ValidationError(
                {"data": "Data inválida. Utilize o formato YYYY-MM-DD."}
            ) from exc
        return Response(montar_grade(laboratorio, data))

    @action(detail=True, methods=["post"])
    def desativar(self, request, pk=None):
        laboratorio = self.get_object()
        laboratorio.ativo = False
        laboratorio.save(update_fields=["ativo"])
        return Response(self.get_serializer(laboratorio).data)

    @action(detail=True, methods=["post"])
    def ativar(self, request, pk=None):
        laboratorio = self.get_object()
        laboratorio.ativo = True
        laboratorio.save(update_fields=["ativo"])
        return Response(self.get_serializer(laboratorio).data)
