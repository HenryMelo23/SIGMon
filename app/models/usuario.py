from dataclasses import dataclass


@dataclass
class Usuario:
    id_usuario: int
    id_departamento: int
    nome: str
    email: str
    matricula: str
    papel: str
    senha_hash: str
    ativo: bool
    data_cadastro: str
