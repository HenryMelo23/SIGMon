from dataclasses import dataclass


@dataclass
class Candidatura:
    id_candidatura: int
    id_edital: int
    id_estudante: int
    id_turma: int
    data_inscricao: str
    ira: float
    nota_disciplina: str
    status: str
    estudante_nome: str = ""
    turma_codigo: str = ""
    disciplina_nome: str = ""
