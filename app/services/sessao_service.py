from app.repositories.alocacao_repository import AlocacaoRepository
from app.repositories.agenda_repository import AgendaRepository
from app.repositories.sessao_repository import SessaoRepository
from app.utils.validators import BusinessError


class SessaoService:
    def __init__(self):
        self.repo = SessaoRepository()
        self.agenda = AgendaRepository()

    def listar(self, usuario):
        if usuario.papel == "ESTUDANTE":
            return self.repo.list_by_estudante(usuario.id_usuario)
        if usuario.papel == "MONITOR":
            alocacoes = AlocacaoRepository().list_by_monitor(usuario.id_usuario)
            alocacao_ids = {a.id_alocacao for a in alocacoes}
            slot_ids = {s.id_slot for s in self.agenda.list_all() if s.id_alocacao in alocacao_ids}
            return [sessao for sessao in self.repo.list_all() if sessao.id_slot in slot_ids]
        if usuario.papel == "PROFESSOR":
            alocacoes = AlocacaoRepository().list_by_professor(usuario.id_usuario)
            alocacao_ids = {a.id_alocacao for a in alocacoes}
            slot_ids = {s.id_slot for s in self.agenda.list_all() if s.id_alocacao in alocacao_ids}
            return [sessao for sessao in self.repo.list_all() if sessao.id_slot in slot_ids]
        return self.repo.list_all()

    def criar_de_slot(self, data):
        slot = self.agenda.get_by_id(data.get("id_slot"))
        if not slot or not slot.reservado:
            raise BusinessError("Sessão só pode ser criada a partir de slot reservado.")
        return self.repo.create(data)

    def marcar_realizada(self, sessao_id):
        return self.repo.update(sessao_id, {"realizada": True})
