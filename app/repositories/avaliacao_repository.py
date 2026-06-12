from app.repositories.base_repository import BaseRepository


class AvaliacaoRepository(BaseRepository):
    dataset_name = "avaliacoes"
    id_field = "id_avaliacao"
