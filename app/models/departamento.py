from dataclasses import dataclass


@dataclass
class Departamento:
    id_departamento: int
    nome: str
    sigla: str
    email: str
