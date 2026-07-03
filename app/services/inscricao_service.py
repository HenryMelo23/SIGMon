from app.repositories.historico_repository import HistoricoRepository
from app.repositories.inscricao_repository import InscricaoRepository
from app.repositories.turma_repository import TurmaRepository
from app.utils.validators import BusinessError


class InscricaoService:
    def __init__(self):
        self.repo = InscricaoRepository()
        self.turmas = TurmaRepository()
        self.historico = HistoricoRepository()

    def listar(self, usuario, filtro=None):
        if usuario.papel == "ADMINISTRADOR":
            if filtro == "aprovada":
                return self.repo.list_by_status("APROVADA")
            return self.repo.list_by_status("PENDENTE")
        return self.repo.list_by_estudante(usuario.id_usuario)

    def obter(self, id_inscricao):
        return self.repo.get_by_id(id_inscricao)

    def cadastrar(self, form, arquivo, id_estudante):
        if not arquivo or arquivo.filename == "":
            raise BusinessError("O comprovante de matrícula (PDF) é obrigatório.")
        conteudo = arquivo.read()
        if len(conteudo) == 0:
            raise BusinessError("O arquivo enviado está vazio.")

        turmas = form.getlist("id_turma")
        if not turmas:
            raise BusinessError("Selecione ao menos uma turma.")

        ids = [int(t) for t in turmas]
        if len(ids) != len(set(ids)):
            raise BusinessError("Há turmas duplicadas na mesma submissão. Remova as repetidas.")

        for id_turma in ids:
            if self.repo.find_ativa_by_estudante_turma(id_estudante, id_turma):
                raise BusinessError("Uma ou mais turmas já possuem inscrição pendente ou aprovada.")
            turma = self.turmas.get_by_id(id_turma)
            if turma and self.historico.find_aprovada_by_estudante_disciplina(id_estudante, turma.id_disciplina):
                raise BusinessError(
                    "Você já foi aprovado nessa disciplina. Não é possível se inscrever em uma turma dela novamente."
                )

        id_documento = self.repo.save_documento(id_estudante, arquivo.filename, conteudo)

        for id_turma in ids:
            self.repo.create({
                "id_estudante": id_estudante,
                "id_turma": id_turma,
                "id_documento": id_documento,
            })

    def aprovar(self, id_inscricao):
        return self.repo.update_status(id_inscricao, "APROVADA")

    def rejeitar(self, id_inscricao, justificativa):
        if not justificativa or not justificativa.strip():
            raise BusinessError("A justificativa é obrigatória ao rejeitar.")
        return self.repo.update_status(id_inscricao, "REJEITADA", justificativa.strip())

    def reverter(self, id_inscricao, justificativa):
        if not justificativa or not justificativa.strip():
            raise BusinessError("A justificativa é obrigatória ao reverter.")
        inscricao = self.repo.get_by_id(id_inscricao)
        if not inscricao or inscricao.status != "APROVADA":
            raise BusinessError("Só é possível reverter inscrições aprovadas.")
        return self.repo.update_status(id_inscricao, "REJEITADA", justificativa.strip())

    def remover(self, id_inscricao, usuario):
        inscricao = self.repo.get_by_id(id_inscricao)
        if not inscricao:
            raise BusinessError("Inscrição não encontrada.")
        if usuario.papel != "ADMINISTRADOR" and inscricao.id_estudante != usuario.id_usuario:
            raise BusinessError("Você não tem permissão para remover esta inscrição.")
        if inscricao.status == "APROVADA":
            raise BusinessError("Inscrições aprovadas não podem ser removidas. Use a opção de reverter.")
        if usuario.papel != "ADMINISTRADOR" and inscricao.status not in ("PENDENTE", "REJEITADA"):
            raise BusinessError("Só é possível remover inscrições pendentes ou rejeitadas.")
        self.repo.delete(id_inscricao)
