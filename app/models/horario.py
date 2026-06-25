from dataclasses import dataclass


@dataclass
class Horario:
    id_horario: int
    codigo: str
    descricao: str
    dias: str
    turno: str
    ativo: bool
