from dataclasses import dataclass


@dataclass
class RegistroFrequencia:
    id_frequencia: int
    id_alocacao: int
    data_atividade: str
    horas: float
    descricao: str
    validado: bool
    id_professor_validador: int | None
