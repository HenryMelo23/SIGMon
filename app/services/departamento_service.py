from app.repositories.departamento_repository import DepartamentoRepository
from app.services.crud_service import CrudService


class DepartamentoService(CrudService):
    repo_class = DepartamentoRepository
