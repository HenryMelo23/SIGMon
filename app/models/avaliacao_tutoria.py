from dataclasses import dataclass


@dataclass
class AvaliacaoTutoria:
    id_avaliacao: int
    id_sessao: int
    id_estudante: int
    nota: int
    comentario: str
    data_avaliacao: str
