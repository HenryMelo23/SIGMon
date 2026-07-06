from dataclasses import dataclass


@dataclass
class InscricaoTurma:
    id_inscricao: int
    id_estudante: int
    id_turma: int
    data_inscricao: str
    status: str
