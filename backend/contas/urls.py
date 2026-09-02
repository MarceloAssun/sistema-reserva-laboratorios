from django.urls import include, path
from rest_framework.routers import DefaultRouter

from contas.views import (
    LoginView,
    RefreshView,
    UsuarioViewSet,
    dashboard,
    logout,
    me,
)

router = DefaultRouter()
router.register("usuarios", UsuarioViewSet, basename="usuario")

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="token_refresh"),
    path("logout/", logout, name="logout"),
    path("me/", me, name="me"),
    path("dashboard/", dashboard, name="dashboard"),
    path("", include(router.urls)),
]
