from app.repositories.historico_repository import HistoricoRepository
from app.utils.validators import BusinessError


class HistoricoService:
    def __init__(self):
        self.repo = HistoricoRepository()

    def listar(self, usuario, filtro=None):
        if usuario.papel == "ADMINISTRADOR":
            if filtro == "aprovado":
                return self.repo.list_by_status("APROVADO")
            return self.repo.list_by_status("PENDENTE")
        return self.repo.list_by_estudante(usuario.id_usuario)

    def listar_aprovadas(self, id_estudante):
        return self.repo.list_aprovadas_by_estudante(id_estudante)

    def obter(self, id_historico):
        return self.repo.get_by_id(id_historico)

    def cadastrar(self, form, arquivo, id_estudante):
        if not arquivo or arquivo.filename == "":
            raise BusinessError("O comprovante (PDF) é obrigatório.")
        conteudo = arquivo.read()
        if len(conteudo) == 0:
            raise BusinessError("O arquivo enviado está vazio.")

        disciplinas = form.getlist("id_disciplina")
        semestres = form.getlist("semestre")
        mencoes = form.getlist("mencao")

        if not disciplinas:
            raise BusinessError("Selecione ao menos uma disciplina.")
        if len(disciplinas) != len(semestres) or len(disciplinas) != len(mencoes):
            raise BusinessError("Dados inconsistentes. Preencha todos os campos.")

        ids = [int(d) for d in disciplinas]
        if len(ids) != len(set(ids)):
            raise BusinessError("Há disciplinas duplicadas na mesma submissão. Remova as repetidas.")

        for id_disciplina in disciplinas:
            if self.repo.find_ativa_by_estudante_disciplina(id_estudante, int(id_disciplina)):
                raise BusinessError("Uma ou mais disciplinas já possuem envio pendente ou aprovado.")

        id_documento = self.repo.save_documento(id_estudante, arquivo.filename, conteudo)

        for id_disciplina, semestre, mencao in zip(disciplinas, semestres, mencoes):
            self.repo.create({
                "id_estudante": id_estudante,
                "id_disciplina": int(id_disciplina),
                "id_documento": id_documento,
                "mencao": mencao.strip().upper(),
                "semestre": semestre.strip(),
            })

    def editar(self, id_historico, form, arquivo, usuario):
        historico = self.repo.get_by_id(id_historico)
        if not historico:
            raise BusinessError("Histórico não encontrado.")
        if historico.id_estudante != usuario.id_usuario:
            raise BusinessError("Você não tem permissão para editar este histórico.")
        if historico.status != "REJEITADO":
            raise BusinessError("Só é possível editar históricos rejeitados.")

        payload = {
            "mencao": form.get("mencao", "").strip().upper(),
            "semestre": form.get("semestre", "").strip(),
            "id_documento": None,
        }

        if arquivo and arquivo.filename != "":
            conteudo = arquivo.read()
            if len(conteudo) > 0:
                payload["id_documento"] = self.repo.save_documento(usuario.id_usuario, arquivo.filename, conteudo)

        self.repo.update(id_historico, payload)

    def aprovar(self, id_historico):
        return self.repo.update_status(id_historico, "APROVADO")

    def rejeitar(self, id_historico, justificativa):
        if not justificativa or not justificativa.strip():
            raise BusinessError("A justificativa é obrigatória ao rejeitar.")
        return self.repo.update_status(id_historico, "REJEITADO", justificativa.strip())

    def reverter(self, id_historico, justificativa):
        if not justificativa or not justificativa.strip():
            raise BusinessError("A justificativa é obrigatória ao reverter.")
        historico = self.repo.get_by_id(id_historico)
        if not historico or historico.status != "APROVADO":
            raise BusinessError("Só é possível reverter históricos aprovados.")
        return self.repo.update_status(id_historico, "REJEITADO", justificativa.strip())

    def remover(self, id_historico, usuario):
        historico = self.repo.get_by_id(id_historico)
        if not historico:
            raise BusinessError("Histórico não encontrado.")
        if usuario.papel != "ADMINISTRADOR" and historico.id_estudante != usuario.id_usuario:
            raise BusinessError("Você não tem permissão para remover este histórico.")
        if historico.status == "APROVADO":
            raise BusinessError("Históricos aprovados não podem ser removidos. Use a opção de reverter.")
        if usuario.papel != "ADMINISTRADOR" and historico.status not in ("PENDENTE", "REJEITADO"):
            raise BusinessError("Só é possível remover históricos pendentes ou rejeitados.")
        self.repo.delete(id_historico)
