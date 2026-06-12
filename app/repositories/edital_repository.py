from app.repositories.base_repository import BaseRepository


class EditalRepository(BaseRepository):
    dataset_name = "editais"
    id_field = "id_edital"
