from dataclasses import dataclass


@dataclass
class Edital:
    id_edital: int
    id_departamento: int
    titulo: str
    descricao: str
    data_inicio: str
    data_fim: str
    quantidade_vagas: int
    nota_minima: float
