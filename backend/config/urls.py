from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from laboratorios.views import LaboratorioViewSet
from reservas.views import ReservaViewSet

router = DefaultRouter()
router.register(r"laboratorios", LaboratorioViewSet, basename="laboratorio")
router.register(r"reservas", ReservaViewSet, basename="reserva")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("contas.urls")),
    path("api/", include(router.urls)),
]
