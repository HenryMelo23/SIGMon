from dataclasses import dataclass


@dataclass
class Turma:
    id_turma: int
    id_disciplina: int
    id_professor: int
    semestre: str
    codigo_turma: str
    tipo_turma: str
    horario: str
    sala: str
