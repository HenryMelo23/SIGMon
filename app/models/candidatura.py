from dataclasses import dataclass


@dataclass
class Candidatura:
    id_candidatura: int
    id_edital: int
    id_estudante: int
    data_inscricao: str
    ira: float
    nota_disciplina: float
    status: str
