GRUPO_ALUNOS = "Alunos"
GRUPO_PROFESSORES = "Professores"
GRUPO_ADMINISTRADORES = "Administradores"

GRUPOS = (GRUPO_ALUNOS, GRUPO_PROFESSORES, GRUPO_ADMINISTRADORES)


def grupos_do_usuario(user):
    if not user or not user.is_authenticated:
        return []
    return list(user.groups.values_list("name", flat=True))


def pertence_ao_grupo(user, nome_grupo):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser and nome_grupo == GRUPO_ADMINISTRADORES:
        return True
    return user.groups.filter(name=nome_grupo).exists()


def is_aluno(user):
    return pertence_ao_grupo(user, GRUPO_ALUNOS)


def is_professor(user):
    return pertence_ao_grupo(user, GRUPO_PROFESSORES)


def is_administrador(user):
    return pertence_ao_grupo(user, GRUPO_ADMINISTRADORES)
