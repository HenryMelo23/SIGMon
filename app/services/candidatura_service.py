from datetime import date

from app.repositories.candidatura_repository import CandidaturaRepository
from app.repositories.edital_repository import EditalRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.edital_service import EditalService
from app.utils.validators import BusinessError


class CandidaturaService:
    def __init__(self):
        self.repo = CandidaturaRepository()
        self.editais = EditalRepository()
        self.edital_service = EditalService()

    def listar(self, usuario, semestre=None, status=None):
        if usuario.papel in ("ESTUDANTE", "MONITOR"):
            return self.repo.list_by_estudante(usuario.id_usuario, semestre=semestre, status=status)
        if usuario.papel == "PROFESSOR":
            return self.repo.list_by_professor(usuario.id_usuario, semestre=semestre, status=status)
        return self.repo.list_all(semestre=semestre, status=status)

    def cancelar(self, candidatura_id, usuario):
        candidatura = self.repo.get_by_id(candidatura_id)
        if not candidatura:
            raise BusinessError("Candidatura não encontrada.")
        if candidatura.id_estudante != usuario.id_usuario:
            raise BusinessError("Você só pode cancelar suas próprias candidaturas.")
        if candidatura.status not in ("INSCRITA", "EM_ANALISE"):
            raise BusinessError("Só é possível cancelar candidaturas com status Inscrita ou Em análise.")
        self.repo.update_status(candidatura_id, "CANCELADA")

    def candidatar(self, edital_id, estudante, data):
        edital = self.editais.get_by_id(edital_id)
        if not edital:
            raise BusinessError("Edital não encontrado.")
        if not self.edital_service.esta_aberto(edital):
            raise BusinessError("Só é possível candidatar-se a edital aberto.")

        id_turma = int(data.get("id_turma"))

        if self.repo.find_aprovada_semestre(estudante.id_usuario, edital.semestre):
            raise BusinessError("Você já foi aprovado como monitor neste semestre.")
        if self.repo.find_by_edital_estudante_turma(edital_id, estudante.id_usuario, id_turma):
            raise BusinessError("Você já se candidatou a esta turma.")

        return self.repo.create({
            "id_edital": int(edital_id),
            "id_estudante": estudante.id_usuario,
            "id_turma": id_turma,
            "data_inscricao": date.today().isoformat(),
            "ira": float(data.get("ira", 0)),
            "nota_disciplina": data.get("nota_disciplina", "").strip().upper(),
            "status": "INSCRITA",
        })

    def alterar_status(self, candidatura_id, status, usuario):
        from app.repositories.turma_repository import TurmaRepository
        if usuario.papel not in {"PROFESSOR", "ADMINISTRADOR"}:
            raise BusinessError("Apenas professor ou administrador pode alterar status.")

        candidatura = self.repo.get_by_id(candidatura_id)
        turma = TurmaRepository().get_by_id(candidatura.id_turma)

        if usuario.papel == "PROFESSOR" and turma.id_professor != usuario.id_usuario:
            raise BusinessError("Você só pode alterar candidaturas das suas turmas.")

        if status == "APROVADA":
            edital = self.editais.get_by_id(candidatura.id_edital)
            if not self.edital_service.esta_aberto(edital):
                raise BusinessError("Não é possível aprovar candidaturas de editais encerrados.")
            if self.repo.find_aprovada_semestre(candidatura.id_estudante, edital.semestre):
                raise BusinessError("Este estudante já foi aprovado como monitor neste semestre.")
            vagas_ocupadas = self.repo.count_aprovadas_turma(candidatura.id_turma, edital.semestre)
            if vagas_ocupadas >= turma.vagas_monitor:
                raise BusinessError("Esta turma não possui mais vagas disponíveis.")
            self.repo.update_status(candidatura_id, status)
            self.repo.cancel_outras(candidatura.id_estudante, edital.semestre, candidatura_id)
            UsuarioRepository().mudar_papel(candidatura.id_estudante, "MONITOR")
        else:
            if candidatura.status == "APROVADA":
                UsuarioRepository().mudar_papel(candidatura.id_estudante, "ESTUDANTE")
            self.repo.update_status(candidatura_id, status)
