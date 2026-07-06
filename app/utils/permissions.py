ROLE_LABELS = {
    "ESTUDANTE": "Estudante",
    "MONITOR": "Monitor",
    "PROFESSOR": "Professor",
    "ADMINISTRADOR": "Administrador",
}

MENU_ITEMS = [
    ("Dashboard", "dashboard.index", {"ESTUDANTE", "MONITOR", "PROFESSOR", "ADMINISTRADOR"}),
    ("Usuários", "usuarios.index", {"ADMINISTRADOR"}),
    ("Departamentos", "departamentos.index", {"ADMINISTRADOR"}),
    ("Disciplinas", "disciplinas.index", {"ADMINISTRADOR"}),
    ("Horários", "horarios.index", {"ADMINISTRADOR"}),
    ("Turmas", "turmas.index", {"PROFESSOR", "ADMINISTRADOR"}),
    ("Histórico Escolar", "historico.index", {"ESTUDANTE", "MONITOR", "ADMINISTRADOR"}),
    ("Inscrições em Turmas", "inscricoes.index", {"ESTUDANTE", "MONITOR", "ADMINISTRADOR"}),
    ("Editais", "editais.index", {"ESTUDANTE", "MONITOR", "PROFESSOR", "ADMINISTRADOR"}),
    ("Candidaturas", "candidaturas.index", {"PROFESSOR", "ADMINISTRADOR"}),
    ("Minhas candidaturas", "candidaturas.minhas", {"ESTUDANTE", "MONITOR"}),
    ("Alocações", "alocacoes.index", {"MONITOR", "PROFESSOR", "ADMINISTRADOR"}),
    ("Agenda", "agenda.index", {"ESTUDANTE", "MONITOR", "PROFESSOR", "ADMINISTRADOR"}),
    ("Sessões", "sessoes.index", {"ESTUDANTE", "MONITOR", "PROFESSOR", "ADMINISTRADOR"}),
    ("Avaliações", "avaliacoes.index", {"ESTUDANTE", "MONITOR", "PROFESSOR", "ADMINISTRADOR"}),
]


def has_role(usuario, roles):
    return usuario and usuario.papel in set(roles)


def menu_for_role(papel):
    return [item for item in MENU_ITEMS if papel in item[2]]
