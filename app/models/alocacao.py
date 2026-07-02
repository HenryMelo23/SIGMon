from dataclasses import dataclass


@dataclass
class AlocacaoMonitor:
    id_alocacao: int
    id_candidatura: int
    id_monitor: int
    id_disciplina: int
    id_turma: int
    id_professor: int
    data_inicio: str
    data_fim: str
    carga_horaria_semanal: int
    status: str
    monitor_nome: str = ""
    disciplina_nome: str = ""
    turma_codigo: str = ""
    professor_nome: str = ""
