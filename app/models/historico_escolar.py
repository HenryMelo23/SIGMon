from dataclasses import dataclass


@dataclass
class HistoricoEscolar:
    id_historico: int
    id_estudante: int
    id_disciplina: int
    id_documento: int
    mencao: str
    semestre: str
    status: str
    justificativa: str
    data_cadastro: str
    disciplina_nome: str = ""
    disciplina_codigo: str = ""
    estudante_nome: str = ""
