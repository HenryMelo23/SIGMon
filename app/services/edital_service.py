from app.repositories.edital_repository import EditalRepository
from app.services.crud_service import CrudService
from app.utils.date_utils import data_entre


class EditalService(CrudService):
    repo_class = EditalRepository
    int_fields = {"id_departamento", "quantidade_vagas"}
    float_fields = {"nota_minima"}

    def listar_com_status(self):
        return [(edital, self.esta_aberto(edital)) for edital in self.listar()]

    def esta_aberto(self, edital):
        return data_entre(edital.data_inicio, edital.data_fim)
