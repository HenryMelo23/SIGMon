from app.repositories.base_repository import BaseRepository


class DadosBancariosRepository(BaseRepository):
    dataset_name = "dados_bancarios"
    id_field = "id_dado_bancario"
