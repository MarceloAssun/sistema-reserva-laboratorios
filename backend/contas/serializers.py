from django.contrib.auth.models import Group, User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from contas.grupos import GRUPOS, grupos_do_usuario


class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate(self, attrs):
        identificador = (attrs.get("username") or attrs.get("email") or "").strip()
        password = attrs.get("password")

        if not identificador or not password:
            raise serializers.ValidationError(
                {"detail": "Informe usuário ou e-mail e senha para entrar."}
            )

        user = User.objects.filter(username__iexact=identificador).first()
        if not user:
            user = User.objects.filter(email__iexact=identificador).first()

        if not user or not user.is_active or not user.check_password(password):
            raise serializers.ValidationError({"detail": "Credenciais inválidas."})

        return super().validate({"username": user.get_username(), "password": password})


class UsuarioSerializer(serializers.ModelSerializer):
    grupos = serializers.SerializerMethodField()
    perfil = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "grupos",
            "perfil",
        )

    def get_grupos(self, obj):
        return grupos_do_usuario(obj)

    def get_perfil(self, obj):
        grupos = grupos_do_usuario(obj)
        if "Administradores" in grupos or obj.is_superuser:
            return "Administrador"
        if "Professores" in grupos:
            return "Professor"
        if "Alunos" in grupos:
            return "Aluno"
        return "Sem perfil"


class AtribuirGrupoSerializer(serializers.Serializer):
    grupo = serializers.ChoiceField(choices=GRUPOS)
