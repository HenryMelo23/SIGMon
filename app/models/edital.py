from dataclasses import dataclass


@dataclass
class Edital:
    id_edital: int
    id_departamento: int
    titulo: str
    descricao: str
    semestre: str
    data_inicio: str
    data_fim: str
    nota_minima: str
    data_inicio_monitoria: str = ""
    data_fim_monitoria: str = ""
