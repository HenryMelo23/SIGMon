from dataclasses import dataclass


@dataclass
class DocumentoAnexo:
    id_documento: int
    id_usuario: int
    nome_arquivo: str
    tipo_documento: str
    mime_type: str
    conteudo: str
    data_upload: str
