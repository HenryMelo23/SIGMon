from app.models import (
    AgendaSlot,
    AlocacaoMonitor,
    AvaliacaoTutoria,
    Candidatura,
    DadosBancarios,
    Departamento,
    Disciplina,
    DocumentoAnexo,
    Edital,
    RegistroFrequencia,
    SessaoTutoria,
    Turma,
    Usuario,
)

DEPARTAMENTOS = [
    Departamento(1, "Departamento de Ciência da Computação", "CIC", "secretaria@cic.unb.br"),
]

USUARIOS = [
    Usuario(1, 1, "Ana Beatriz Martins", "admin@unb.br", "ADM001", "ADMINISTRADOR", "123456", True, "2026-01-10"),
    Usuario(2, 1, "Prof. Rafael Nogueira", "professor@unb.br", "DOC742", "PROFESSOR", "123456", True, "2026-01-11"),
    Usuario(3, 1, "Luísa Carvalho", "estudante@unb.br", "231045678", "ESTUDANTE", "123456", True, "2026-02-02"),
    Usuario(4, 1, "Mateus Henrique Lima", "monitor@unb.br", "211098765", "MONITOR", "123456", True, "2026-02-08"),
    Usuario(5, 1, "Camila Rocha", "financeiro@unb.br", "FIN018", "FINANCEIRO", "123456", True, "2026-01-20"),
    Usuario(6, 1, "Usuário Inativo", "inativo@unb.br", "000000000", "ESTUDANTE", "123456", False, "2026-01-22"),
]

DISCIPLINAS = [
    Disciplina(1, 1, "CIC0097", "Banco de Dados", 4),
    Disciplina(2, 1, "CIC0105", "Estruturas de Dados", 4),
    Disciplina(3, 1, "CIC0004", "Algoritmos", 4),
]

TURMAS = [
    Turma(1, 1, 2, "2026.1", "A", "TEORICA", "Seg/Qua 10:00-11:50", "PJC BT 036"),
    Turma(2, 2, 2, "2026.1", "B", "PRATICA", "Ter/Qui 14:00-15:50", "LAB CIC 02"),
    Turma(3, 3, 2, "2026.1", "C", "TEORICA", "Sex 08:00-11:50", "PJC BT 044"),
]

EDITAIS = [
    Edital(1, 1, "Edital de Monitoria CIC 2026.1", "Seleção para monitoria remunerada e voluntária em disciplinas do CIC.", "2026-06-01", "2026-07-20", 8, 7.0),
    Edital(2, 1, "Edital Complementar Banco de Dados", "Chamada complementar para apoio em laboratório e atendimento aos estudantes.", "2026-04-01", "2026-04-30", 2, 7.5),
]

CANDIDATURAS = [
    Candidatura(1, 1, 3, "2026-06-05", 4.35, 8.7, "INSCRITA"),
    Candidatura(2, 2, 4, "2026-04-08", 4.62, 9.1, "APROVADA"),
    Candidatura(3, 2, 3, "2026-04-10", 3.95, 6.8, "REPROVADA"),
]

ALOCACOES = [
    AlocacaoMonitor(1, 2, 4, 1, 1, 2, "2026-05-01", "2026-08-31", 12, "ATIVA"),
]

DADOS_BANCARIOS = [
    DadosBancarios(1, 4, "Banco do Brasil", "3602-1", "128934-5", "CORRENTE", "mateus.lima@aluno.unb.br", "2026-05-02"),
]

DOCUMENTOS_ANEXOS = [
    DocumentoAnexo(1, 3, 1, 1, "historico_luisa.pdf", "Histórico Escolar", "application/pdf", "conteudo-simulado-base64", "2026-06-05"),
]

AGENDA_SLOTS = [
    AgendaSlot(1, 1, "2026-06-12", "14:00", "15:00", "Laboratório CIC 02", "PRESENCIAL", False),
    AgendaSlot(2, 1, "2026-06-13", "09:00", "10:00", "Google Meet", "ONLINE", True),
    AgendaSlot(3, 1, "2026-06-14", "16:00", "17:00", "Laboratório CIC 01", "HIBRIDA", False),
]

SESSOES = [
    SessaoTutoria(1, 2, 3, "Modelagem ER", "Dúvidas sobre cardinalidade e normalização.", False, "2026-06-10"),
    SessaoTutoria(2, 2, 3, "SQL Joins", "Atendimento concluído com exercícios práticos.", True, "2026-06-08"),
]

FREQUENCIAS = [
    RegistroFrequencia(1, 1, "2026-06-08", 2.0, "Atendimento de dúvidas sobre SQL e revisão de listas.", True, 2),
    RegistroFrequencia(2, 1, "2026-06-10", 1.5, "Preparação de material de apoio para laboratório.", False, None),
]

AVALIACOES = [
    AvaliacaoTutoria(1, 2, 3, 5, "Atendimento claro, objetivo e muito útil.", "2026-06-09"),
]

DATASETS = {
    "departamentos": DEPARTAMENTOS,
    "usuarios": USUARIOS,
    "disciplinas": DISCIPLINAS,
    "turmas": TURMAS,
    "editais": EDITAIS,
    "candidaturas": CANDIDATURAS,
    "alocacoes": ALOCACOES,
    "dados_bancarios": DADOS_BANCARIOS,
    "documentos": DOCUMENTOS_ANEXOS,
    "agenda": AGENDA_SLOTS,
    "sessoes": SESSOES,
    "frequencias": FREQUENCIAS,
    "avaliacoes": AVALIACOES,
}
