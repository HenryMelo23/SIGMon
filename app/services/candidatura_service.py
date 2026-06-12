from datetime import date

from app.repositories.candidatura_repository import CandidaturaRepository
from app.repositories.edital_repository import EditalRepository
from app.services.edital_service import EditalService
from app.utils.audit import registrar_auditoria
from app.utils.validators import BusinessError


class CandidaturaService:
    def __init__(self):
        self.repo = CandidaturaRepository()
        self.editais = EditalRepository()
        self.edital_service = EditalService()

    def listar(self, usuario):
        if usuario.papel == "ESTUDANTE":
            return self.repo.list_by_estudante(usuario.id_usuario)
        return self.repo.list_all()

    def candidatar(self, edital_id, estudante, data):
        edital = self.editais.get_by_id(edital_id)
        if not edital:
            raise BusinessError("Edital não encontrado.")
        if not self.edital_service.esta_aberto(edital):
            raise BusinessError("Só é possível candidatar-se a edital aberto.")
        if self.repo.find_by_edital_estudante(edital_id, estudante.id_usuario):
            raise BusinessError("Você já se candidatou a este edital.")
        return self.repo.create(
            {
                "id_edital": int(edital_id),
                "id_estudante": estudante.id_usuario,
                "data_inscricao": date.today().isoformat(),
                "ira": float(data.get("ira", 0)),
                "nota_disciplina": float(data.get("nota_disciplina", 0)),
                "status": "INSCRITA",
            }
        )

    def alterar_status(self, candidatura_id, status, usuario):
        if usuario.papel not in {"PROFESSOR", "ADMINISTRADOR"}:
            raise BusinessError("Apenas professor ou administrador pode alterar status.")
        candidatura = self.repo.update(candidatura_id, {"status": status})
        registrar_auditoria(usuario.id_usuario, "ALTERAR_STATUS_CANDIDATURA", "Candidatura", f"{candidatura_id} -> {status}")
        return candidatura
