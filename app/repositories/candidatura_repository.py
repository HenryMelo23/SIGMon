from app.repositories.base_repository import BaseRepository


class CandidaturaRepository(BaseRepository):
    dataset_name = "candidaturas"
    id_field = "id_candidatura"

    def list_by_estudante(self, estudante_id):
        return [c for c in self.items if c.id_estudante == int(estudante_id)]

    def find_by_edital_estudante(self, edital_id, estudante_id):
        return next(
            (c for c in self.items if c.id_edital == int(edital_id) and c.id_estudante == int(estudante_id)),
            None,
        )
