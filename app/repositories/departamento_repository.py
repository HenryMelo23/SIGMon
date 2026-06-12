from app.repositories.base_repository import BaseRepository


class DepartamentoRepository(BaseRepository):
    dataset_name = "departamentos"
    id_field = "id_departamento"
