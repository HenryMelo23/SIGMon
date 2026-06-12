from app.repositories.disciplina_repository import DisciplinaRepository
from app.services.crud_service import CrudService


class DisciplinaService(CrudService):
    repo_class = DisciplinaRepository
    int_fields = {"id_departamento", "creditos"}
