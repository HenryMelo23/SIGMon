from app.repositories.base_repository import BaseRepository


class TurmaRepository(BaseRepository):
    dataset_name = "turmas"
    id_field = "id_turma"
