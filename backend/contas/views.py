from datetime import date

from django.contrib.auth.models import Group, User
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from contas.grupos import grupos_do_usuario, is_administrador, is_aluno, is_professor
from contas.permissions import IsAdministrador
from contas.serializers import AtribuirGrupoSerializer, LoginSerializer, UsuarioSerializer
from laboratorios.models import Laboratorio
from reservas.models import Reserva, StatusReserva


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer


class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    data = UsuarioSerializer(request.user).data
    data["is_superuser"] = request.user.is_superuser
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    from rest_framework_simplejwt.tokens import RefreshToken
    from rest_framework_simplejwt.exceptions import TokenError

    refresh = request.data.get("refresh")
    if not refresh:
        return Response(
            {"detail": "Informe o refresh token para encerrar a sessão."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        token = RefreshToken(refresh)
        token.blacklist()
    except TokenError:
        return Response(
            {"detail": "Refresh token inválido ou já encerrado."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response({"detail": "Sessão encerrada."})


class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by("username")
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, IsAdministrador]

    @action(detail=True, methods=["post"], url_path="atribuir-grupo")
    def atribuir_grupo(self, request, pk=None):
        usuario = self.get_object()
        serializer = AtribuirGrupoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        grupo = Group.objects.get(name=serializer.validated_data["grupo"])
        usuario.groups.clear()
        usuario.groups.add(grupo)
        return Response(UsuarioSerializer(usuario).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = request.user
    hoje = date.today()

    if is_administrador(user):
        return Response(
            {
                "perfil": "Administrador",
                "total_laboratorios": Laboratorio.objects.count(),
                "laboratorios_ativos": Laboratorio.objects.filter(ativo=True).count(),
                "solicitacoes_pendentes": Reserva.objects.filter(
                    status=StatusReserva.PENDENTE
                ).count(),
                "reservas_aprovadas": Reserva.objects.filter(
                    status=StatusReserva.APROVADA
                ).count(),
            }
        )

    if is_professor(user):
        minhas = Reserva.objects.filter(professor=user)
        proximas = (
            minhas.filter(status=StatusReserva.APROVADA, data__gte=hoje)
            .order_by("data", "hora_inicio")[:5]
        )
        from reservas.serializers import ReservaSerializer

        return Response(
            {
                "perfil": "Professor",
                "total_reservas": minhas.count(),
                "reservas_pendentes": minhas.filter(status=StatusReserva.PENDENTE).count(),
                "reservas_aprovadas": minhas.filter(status=StatusReserva.APROVADA).count(),
                "proximas_reservas": ReservaSerializer(proximas, many=True).data,
            }
        )

    if is_aluno(user):
        return Response(
            {
                "perfil": "Aluno",
                "laboratorios_ativos": Laboratorio.objects.filter(ativo=True).count(),
                "laboratorios": list(
                    Laboratorio.objects.filter(ativo=True).values(
                        "id", "nome", "bloco", "capacidade"
                    )
                ),
            }
        )

    return Response(
        {
            "perfil": "Sem perfil",
            "grupos": grupos_do_usuario(user),
            "detail": "Seu usuário ainda não possui um perfil (grupo) atribuído.",
        }
    )
