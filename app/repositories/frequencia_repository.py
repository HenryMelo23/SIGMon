from app.repositories.base_repository import BaseRepository


class FrequenciaRepository(BaseRepository):
    dataset_name = "frequencias"
    id_field = "id_frequencia"

    def list_validadas(self):
        return [f for f in self.items if f.validado]
