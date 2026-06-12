from dataclasses import dataclass


@dataclass
class Disciplina:
    id_disciplina: int
    id_departamento: int
    codigo: str
    nome: str
    creditos: int
