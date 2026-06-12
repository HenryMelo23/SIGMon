from app.repositories.base_repository import BaseRepository


class AgendaRepository(BaseRepository):
    dataset_name = "agenda"
    id_field = "id_slot"

    def list_disponiveis(self):
        return [s for s in self.items if not s.reservado]
