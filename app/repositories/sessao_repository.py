from app.repositories.base_repository import BaseRepository


class SessaoRepository(BaseRepository):
    dataset_name = "sessoes"
    id_field = "id_sessao"

    def list_by_estudante(self, estudante_id):
        return [s for s in self.items if s.id_estudante == int(estudante_id)]
