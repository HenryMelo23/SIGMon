from dataclasses import dataclass


@dataclass
class DocumentoAnexo:
    id_documento: int
    id_usuario: int
    id_edital: int
    id_candidatura: int
    nome_arquivo: str
    tipo_documento: str
    mime_type: str
    conteudo: str
    data_upload: str
