from django.urls import path
from rest_framework.routers import DefaultRouter

from laboratorios.views import LaboratorioViewSet

router = DefaultRouter()
router.register("", LaboratorioViewSet, basename="laboratorio")

urlpatterns = router.urls
