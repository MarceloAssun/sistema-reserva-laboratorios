from rest_framework.permissions import BasePermission, SAFE_METHODS

from contas.grupos import is_administrador, is_aluno, is_professor


class IsAdministrador(BasePermission):
    message = "Apenas administradores podem realizar esta ação."

    def has_permission(self, request, view):
        return is_administrador(request.user)


class IsProfessor(BasePermission):
    message = "Apenas professores podem realizar esta ação."

    def has_permission(self, request, view):
        return is_professor(request.user)


class IsAluno(BasePermission):
    def has_permission(self, request, view):
        return is_aluno(request.user)


class IsProfessorOuAdministrador(BasePermission):
    def has_permission(self, request, view):
        return is_professor(request.user) or is_administrador(request.user)


class LaboratorioPermission(BasePermission):
    message = "Você não tem permissão para gerenciar laboratórios."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return is_administrador(request.user)


class ReservaPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        acao = getattr(view, "action", None)
        if acao == "create":
            return is_professor(request.user)
        if acao in ("aprovar", "rejeitar"):
            return is_administrador(request.user)
        if request.method in SAFE_METHODS:
            return is_professor(request.user) or is_administrador(request.user)
        return is_professor(request.user) or is_administrador(request.user)

    def has_object_permission(self, request, view, obj):
        if is_administrador(request.user):
            return True
        if is_professor(request.user):
            return obj.professor_id == request.user.id
        return False
