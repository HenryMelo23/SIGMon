from dataclasses import dataclass


@dataclass
class InscricaoTurma:
    id_inscricao: int
    id_estudante: int
    id_turma: int
    id_documento: int
    status: str
    justificativa: str
    data_cadastro: str
    estudante_nome: str = ""
    turma_codigo: str = ""
    disciplina_nome: str = ""
    semestre: str = ""
