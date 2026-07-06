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
    Departamento(1, "Departamento de Ciencia da Computacao", "CIC", "secretaria@cic.unb.br"),
]

USUARIOS = [
    Usuario(1, 1, "Ana Beatriz Martins", "admin@unb.br", "ADM001", "ADMINISTRADOR", "123456", True, "2026-01-10"),
    Usuario(2, 1, "Pedro Alves", "pedro@unb.br", "230078934", "ESTUDANTE", "123456", True, "2026-02-12"),
    Usuario(3, 1, "Prof. Caetano Silva", "professor@unb.br", "DOC742", "PROFESSOR", "123456", True, "2026-01-11"),
    Usuario(4, 1, "Amanda Souza", "amanda@unb.br", "231045678", "ESTUDANTE", "123456", True, "2026-02-02"),
    Usuario(5, 1, "Camila Rocha", "financeiro@unb.br", "FIN018", "FINANCEIRO", "123456", True, "2026-01-20"),
    Usuario(6, 1, "Rafael Nogueira", "rafael@unb.br", "211098765", "MONITOR", "123456", True, "2026-02-08"),
]

DISCIPLINAS = [
    Disciplina(1, 1, "CIC0097", "Banco de Dados", 4, "CIC"),
    Disciplina(2, 1, "CIC0105", "Estruturas de Dados", 4, "CIC"),
    Disciplina(3, 1, "CIC0004", "Algoritmos", 4, "CIC"),
]

TURMAS = [
    Turma(1, 1, 3, "2026.1", "T01", 1, "PJC BT 036", 1, "Banco de Dados", "Prof. Caetano Silva", "246M34"),
    Turma(2, 2, 3, "2026.1", "T01", 2, "LAB CIC 02", 1, "Estruturas de Dados", "Prof. Caetano Silva", "35T23"),
    Turma(3, 3, 3, "2026.1", "T01", 3, "PJC BT 044", 2, "Algoritmos", "Prof. Caetano Silva", "6M1234"),
]

EDITAIS = [
    Edital(1, 1, "Edital de Monitoria CIC 2026.1", "Selecao para monitoria remunerada.", "2026.1", "2026-06-01", "2026-07-20", "MS"),
    Edital(2, 1, "Edital Complementar Banco de Dados", "Chamada complementar para apoio em laboratorio.", "2026.1", "2026-04-01", "2026-04-30", "MS"),
]

CANDIDATURAS = [
    Candidatura(1, 1, 2, 2, "2026-06-05", 4.35, "SS", "INSCRITA"),
    Candidatura(2, 2, 6, 1, "2026-04-08", 4.62, "SS", "APROVADA"),
    Candidatura(3, 2, 4, 1, "2026-04-10", 3.95, "MM", "REPROVADA"),
]

ALOCACOES = [
    AlocacaoMonitor(1, 2, 6, 1, 1, 3, "2026-05-01", "2026-08-31", 12, "ATIVA"),
]

DADOS_BANCARIOS = [
    DadosBancarios(1, 6, "Banco do Brasil", "3602-1", "128934-5", "CORRENTE", "rafael@aluno.unb.br", "2026-05-02"),
]

DOCUMENTOS_ANEXOS = [
    DocumentoAnexo(1, 2, 1, 1, "historico_pedro.pdf", "Historico Escolar", "application/pdf", "conteudo-simulado-base64", "2026-06-05"),
]

AGENDA_SLOTS = [
    AgendaSlot(1, 1, "2026-06-12", "14:00", "15:00", "Laboratorio CIC 02", "PRESENCIAL", False),
    AgendaSlot(2, 1, "2026-06-13", "09:00", "10:00", "Google Meet", "ONLINE", True),
    AgendaSlot(3, 1, "2026-06-14", "16:00", "17:00", "Laboratorio CIC 01", "HIBRIDA", False),
]

SESSOES = [
    SessaoTutoria(1, 1, 4, "Modelagem ER", "Duvidas sobre cardinalidade e normalizacao.", True, "2026-06-10"),
    SessaoTutoria(2, 2, 4, "SQL Joins", "Atendimento concluido com exercicios praticos.", True, "2026-06-08"),
]

FREQUENCIAS = [
    RegistroFrequencia(1, 1, "2026-06-08", 2.0, "Atendimento de duvidas sobre SQL.", True, 3),
    RegistroFrequencia(2, 1, "2026-06-10", 1.5, "Preparacao de material de apoio.", False, None),
]

AVALIACOES = [
    AvaliacaoTutoria(1, 1, 4, 5, "Atendimento claro e objetivo.", "2026-06-09"),
    AvaliacaoTutoria(2, 2, 4, 4, "Boa explicacao.", "2026-06-10"),
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
