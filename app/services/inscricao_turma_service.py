from app.repositories.inscricao_turma_repository import InscricaoTurmaRepository
from app.utils.validators import BusinessError


class InscricaoTurmaService:
    def __init__(self):
        self.repo = InscricaoTurmaRepository()

    def listar(self, usuario):
        if usuario.papel == "ADMINISTRADOR":
            return self.repo.list_all()
        return self.repo.list_by_estudante(usuario.id_usuario)

    def solicitar(self, usuario, data):
        id_turma = int(data.get("id_turma"))
        existente = self.repo.find_by_estudante_turma(usuario.id_usuario, id_turma)
        if existente:
            raise BusinessError("Voce ja possui uma inscricao para esta turma.")
        return self.repo.create({"id_estudante": usuario.id_usuario, "id_turma": id_turma})

    def alterar_status(self, id_inscricao, status):
        if status not in {"PENDENTE", "APROVADA", "REJEITADA", "CANCELADA"}:
            raise BusinessError("Status de inscricao invalido.")
        return self.repo.update_status(id_inscricao, status)
