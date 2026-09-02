from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from contas.grupos import GRUPOS, GRUPO_ADMINISTRADORES, GRUPO_ALUNOS, GRUPO_PROFESSORES
from laboratorios.models import Laboratorio


USUARIOS_DEMO = [
    {
        "username": "aluno",
        "first_name": "Ana",
        "last_name": "Aluna",
        "email": "aluno@demo.local",
        "grupo": GRUPO_ALUNOS,
    },
    {
        "username": "professor",
        "first_name": "Paulo",
        "last_name": "Professor",
        "email": "professor@demo.local",
        "grupo": GRUPO_PROFESSORES,
    },
    {
        "username": "admin",
        "first_name": "Alice",
        "last_name": "Administradora",
        "email": "admin@demo.local",
        "grupo": GRUPO_ADMINISTRADORES,
        "is_staff": True,
        "is_superuser": True,
    },
]

LABORATORIOS_DEMO = [
    {"nome": "Laboratório de Informática 01", "capacidade": 30, "bloco": "A"},
    {"nome": "Laboratório de Informática 02", "capacidade": 25, "bloco": "A"},
    {"nome": "Laboratório de Eletrônica", "capacidade": 20, "bloco": "B"},
]


class Command(BaseCommand):
    help = "Cria grupos, usuários de demonstração e laboratórios de exemplo."

    def handle(self, *args, **options):
        senha = settings.DEMO_PASSWORD

        for nome in GRUPOS:
            Group.objects.get_or_create(name=nome)
            self.stdout.write(f"Grupo garantido: {nome}")

        for dados in USUARIOS_DEMO:
            grupo = Group.objects.get(name=dados["grupo"])
            user, created = User.objects.get_or_create(
                username=dados["username"],
                defaults={
                    "first_name": dados["first_name"],
                    "last_name": dados["last_name"],
                    "email": dados["email"],
                    "is_staff": dados.get("is_staff", False),
                    "is_superuser": dados.get("is_superuser", False),
                },
            )
            user.set_password(senha)
            user.first_name = dados["first_name"]
            user.last_name = dados["last_name"]
            user.email = dados["email"]
            user.is_staff = dados.get("is_staff", False)
            user.is_superuser = dados.get("is_superuser", False)
            user.save()
            user.groups.clear()
            user.groups.add(grupo)
            acao = "criado" if created else "atualizado"
            self.stdout.write(f"Usuário {acao}: {user.username} ({dados['grupo']})")

        for lab in LABORATORIOS_DEMO:
            obj, created = Laboratorio.objects.get_or_create(
                nome=lab["nome"],
                defaults={"capacidade": lab["capacidade"], "bloco": lab["bloco"]},
            )
            acao = "criado" if created else "já existia"
            self.stdout.write(f"Laboratório {acao}: {obj.nome}")

        self.stdout.write(self.style.SUCCESS("Dados de demonstração prontos."))
        self.stdout.write(
            "Usuários: aluno, professor, admin — senha definida em DEMO_PASSWORD no .env"
        )
