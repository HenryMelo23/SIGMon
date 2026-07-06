from dataclasses import dataclass


@dataclass
class Turma:
    id_turma: int
    id_disciplina: int
    id_professor: int
    semestre: str
    codigo_turma: str
    id_horario: int
    sala: str
    vagas_monitor: int = 0
    carga_horaria_semanal: int = 12
    disciplina_nome: str = ""
    professor_nome: str = ""
    horario_codigo: str = ""
    mencao_estudante: str = ""
    vagas_disponiveis: int = 0
