from dataclasses import dataclass


@dataclass
class AgendaSlot:
    id_slot: int
    id_alocacao: int
    data_slot: str
    hora_inicio: str
    hora_fim: str
    local_atendimento: str
    modalidade: str
    reservado: bool
    monitor_nome: str = ""
    disciplina_nome: str = ""
    turma_codigo: str = ""
