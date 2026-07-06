from datetime import date

from app.repositories.agenda_repository import AgendaRepository
from app.repositories.alocacao_repository import AlocacaoRepository
from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.repositories.sessao_repository import SessaoRepository
from app.utils.validators import BusinessError


class AvaliacaoService:
    def __init__(self):
        self.repo = AvaliacaoRepository()
        self.sessoes = SessaoRepository()

    def listar(self, usuario):
        avaliacoes = self.repo.list_all()
        if usuario.papel == "ESTUDANTE":
            return [a for a in avaliacoes if a.id_estudante == usuario.id_usuario]
        if usuario.papel == "MONITOR":
            alocacoes = AlocacaoRepository().list_by_monitor(usuario.id_usuario)
            alocacao_ids = {a.id_alocacao for a in alocacoes}
            slots = AgendaRepository().list_all()
            slot_ids = {s.id_slot for s in slots if s.id_alocacao in alocacao_ids}
            sessoes = self.sessoes.list_all()
            sessao_ids = {s.id_sessao for s in sessoes if s.id_slot in slot_ids}
            return [a for a in avaliacoes if a.id_sessao in sessao_ids]
        return avaliacoes

    def desempenho_por_disciplina(self, usuario):
        if usuario.papel == "MONITOR":
            return self.repo.desempenho_por_disciplina(usuario.id_usuario)
        if usuario.papel in {"PROFESSOR", "ADMINISTRADOR"}:
            return self.repo.desempenho_por_disciplina()
        return []

    def criar(self, sessao_id, estudante, data):
        sessao = self.sessoes.get_by_id(sessao_id)
        if not sessao or not sessao.realizada:
            raise BusinessError("A avaliação só pode ser feita para sessão realizada.")
        return self.repo.create(
            {
                "id_sessao": int(sessao_id),
                "id_estudante": estudante.id_usuario,
                "nota": int(data["nota"]),
                "comentario": data.get("comentario", ""),
                "data_avaliacao": date.today().isoformat(),
            }
        )
