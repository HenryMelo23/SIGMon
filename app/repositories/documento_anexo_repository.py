from app.repositories.base_repository import BaseRepository


class DocumentoAnexoRepository(BaseRepository):
    dataset_name = "documentos"
    id_field = "id_documento"
