from app.repositories.turma_repository import TurmaRepository
from app.services.crud_service import CrudService


class TurmaService(CrudService):
    repo_class = TurmaRepository
    int_fields = {"id_disciplina", "id_professor"}
