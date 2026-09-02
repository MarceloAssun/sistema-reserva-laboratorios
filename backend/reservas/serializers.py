from rest_framework import serializers

from contas.grupos import is_professor
from reservas.models import Reserva


class ReservaSerializer(serializers.ModelSerializer):
    laboratorio_nome = serializers.CharField(source="laboratorio.nome", read_only=True)
    professor_nome = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Reserva
        fields = (
            "id",
            "laboratorio",
            "laboratorio_nome",
            "professor",
            "professor_nome",
            "data",
            "hora_inicio",
            "hora_fim",
            "status",
            "status_display",
            "observacao",
            "data_solicitacao",
        )
        read_only_fields = ("professor", "status", "data_solicitacao")

    def get_professor_nome(self, obj):
        nome = obj.professor.get_full_name().strip()
        return nome or obj.professor.username

    def validate(self, attrs):
        hora_inicio = attrs.get("hora_inicio")
        hora_fim = attrs.get("hora_fim")
        laboratorio = attrs.get("laboratorio")

        if hora_inicio and hora_fim and hora_fim <= hora_inicio:
            raise serializers.ValidationError(
                {"hora_fim": "A hora de término deve ser posterior à hora de início."}
            )

        if laboratorio and not laboratorio.ativo:
            raise serializers.ValidationError(
                {"laboratorio": "Não é possível reservar um laboratório inativo."}
            )

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        if not is_professor(request.user):
            raise serializers.ValidationError(
                "Somente professores podem solicitar reservas."
            )
        validated_data["professor"] = request.user
        return super().create(validated_data)
