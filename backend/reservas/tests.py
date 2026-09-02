from datetime import date, time, timedelta

from django.contrib.auth.models import Group, User
from rest_framework import status
from rest_framework.test import APITestCase

from contas.grupos import GRUPO_ADMINISTRADORES, GRUPO_ALUNOS, GRUPO_PROFESSORES
from laboratorios.models import Laboratorio
from reservas.models import Reserva, StatusReserva


class ReservaAPITests(APITestCase):
    def setUp(self):
        self.grupo_aluno = Group.objects.create(name=GRUPO_ALUNOS)
        self.grupo_prof = Group.objects.create(name=GRUPO_PROFESSORES)
        self.grupo_admin = Group.objects.create(name=GRUPO_ADMINISTRADORES)

        self.aluno = User.objects.create_user("aluno", password="teste12345")
        self.aluno.groups.add(self.grupo_aluno)

        self.professor = User.objects.create_user(
            "professor",
            password="teste12345",
            first_name="Paulo",
            email="professor@demo.local",
        )
        self.professor.groups.add(self.grupo_prof)

        self.admin = User.objects.create_user("admin", password="teste12345")
        self.admin.groups.add(self.grupo_admin)

        self.lab = Laboratorio.objects.create(
            nome="Lab Teste", capacidade=20, bloco="A", ativo=True
        )
        self.lab_inativo = Laboratorio.objects.create(
            nome="Lab Inativo", capacidade=10, bloco="B", ativo=False
        )
        self.data = date.today() + timedelta(days=7)

    def autenticar(self, user):
        resp = self.client.post(
            "/api/login/",
            {"username": user.username, "password": "teste12345"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")

    def payload(self, **kwargs):
        dados = {
            "laboratorio": self.lab.id,
            "data": self.data.isoformat(),
            "hora_inicio": "08:00:00",
            "hora_fim": "10:00:00",
            "observacao": "Aula prática",
        }
        dados.update(kwargs)
        return dados

    def test_aluno_consulta_laboratorio_mas_nao_cria_reserva(self):
        self.autenticar(self.aluno)
        labs = self.client.get("/api/laboratorios/")
        self.assertEqual(labs.status_code, status.HTTP_200_OK)
        criar = self.client.post("/api/reservas/", self.payload(), format="json")
        self.assertEqual(criar.status_code, status.HTTP_403_FORBIDDEN)

    def test_professor_cria_reserva_pendente(self):
        self.autenticar(self.professor)
        resp = self.client.post("/api/reservas/", self.payload(), format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["status"], StatusReserva.PENDENTE)
        self.assertEqual(resp.data["professor"], self.professor.id)

    def test_nao_reserva_laboratorio_inativo(self):
        self.autenticar(self.professor)
        resp = self.client.post(
            "/api/reservas/",
            self.payload(laboratorio=self.lab_inativo.id),
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_hora_fim_deve_ser_posterior(self):
        self.autenticar(self.professor)
        resp = self.client.post(
            "/api/reservas/",
            self.payload(hora_inicio="10:00:00", hora_fim="09:00:00"),
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_aprova_e_bloqueia_conflito(self):
        self.autenticar(self.professor)
        r1 = self.client.post("/api/reservas/", self.payload(), format="json")
        r2 = self.client.post(
            "/api/reservas/",
            self.payload(hora_inicio="09:00:00", hora_fim="11:00:00"),
            format="json",
        )
        self.assertEqual(r1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r2.status_code, status.HTTP_201_CREATED)

        self.autenticar(self.admin)
        ok = self.client.post(f"/api/reservas/{r1.data['id']}/aprovar/")
        self.assertEqual(ok.status_code, status.HTTP_200_OK)
        self.assertEqual(ok.data["status"], StatusReserva.APROVADA)

        conflito = self.client.post(f"/api/reservas/{r2.data['id']}/aprovar/")
        self.assertEqual(conflito.status_code, status.HTTP_400_BAD_REQUEST)

    def test_professor_cancela_propria_reserva(self):
        self.autenticar(self.professor)
        criada = self.client.post("/api/reservas/", self.payload(), format="json")
        cancelada = self.client.post(f"/api/reservas/{criada.data['id']}/cancelar/")
        self.assertEqual(cancelada.status_code, status.HTTP_200_OK)
        self.assertEqual(cancelada.data["status"], StatusReserva.CANCELADA)
        self.assertTrue(Reserva.objects.filter(pk=criada.data["id"]).exists())

    def test_professor_nao_aprova(self):
        self.autenticar(self.professor)
        criada = self.client.post("/api/reservas/", self.payload(), format="json")
        aprovar = self.client.post(f"/api/reservas/{criada.data['id']}/aprovar/")
        self.assertEqual(aprovar.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_aceita_email_ou_username(self):
        resp = self.client.post(
            "/api/login/",
            {"username": self.professor.email, "password": "teste12345"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.data)

    def test_disponibilidade_marca_horario_ocupado_apos_aprovacao(self):
        Reserva.objects.create(
            laboratorio=self.lab,
            professor=self.professor,
            data=self.data,
            hora_inicio=time(8, 0),
            hora_fim=time(10, 0),
            status=StatusReserva.APROVADA,
        )
        self.autenticar(self.aluno)
        resp = self.client.get(
            f"/api/laboratorios/{self.lab.id}/disponibilidade/?data={self.data.isoformat()}"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        slot = next(
            item
            for item in resp.data["grade"]
            if item["hora_inicio"] == "08:00"
        )
        self.assertTrue(slot["ocupado"])
