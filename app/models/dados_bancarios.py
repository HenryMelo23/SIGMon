from dataclasses import dataclass


@dataclass
class DadosBancarios:
    id_dado_bancario: int
    id_usuario: int
    banco: str
    agencia: str
    conta: str
    tipo_conta: str
    chave_pix: str
    atualizado_em: str
