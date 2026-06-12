from app.repositories.alocacao_repository import AlocacaoRepository
from app.repositories.candidatura_repository import CandidaturaRepository
from app.utils.validators import BusinessError


class AlocacaoService:
    def __init__(self):
        self.repo = AlocacaoRepository()
        self.candidaturas = CandidaturaRepository()

    def listar(self, usuario):
        if usuario.papel == "MONITOR":
            return self.repo.list_by_monitor(usuario.id_usuario)
        if usuario.papel == "PROFESSOR":
            return self.repo.list_by_professor(usuario.id_usuario)
        return self.repo.list_all()

    def criar(self, data):
        candidatura = self.candidaturas.get_by_id(data.get("id_candidatura"))
        if not candidatura or candidatura.status != "APROVADA":
            raise BusinessError("Apenas candidatura aprovada pode gerar alocação.")
        payload = dict(data)
        for key in ["id_candidatura", "id_monitor", "id_disciplina", "id_turma", "id_professor", "carga_horaria_semanal"]:
            payload[key] = int(payload[key])
        payload["status"] = payload.get("status") or "ATIVA"
        return self.repo.create(payload)

    def alterar_status(self, alocacao_id, status):
        return self.repo.update(alocacao_id, {"status": status})
