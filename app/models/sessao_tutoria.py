from dataclasses import dataclass


@dataclass
class SessaoTutoria:
    id_sessao: int
    id_slot: int
    id_estudante: int
    assunto: str
    realizada: bool
    data_registro: str
