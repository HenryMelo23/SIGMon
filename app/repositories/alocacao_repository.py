from app.repositories.base_repository import BaseRepository


class AlocacaoRepository(BaseRepository):
    dataset_name = "alocacoes"
    id_field = "id_alocacao"

    def list_by_monitor(self, monitor_id):
        return [a for a in self.items if a.id_monitor == int(monitor_id)]

    def list_by_professor(self, professor_id):
        return [a for a in self.items if a.id_professor == int(professor_id)]
