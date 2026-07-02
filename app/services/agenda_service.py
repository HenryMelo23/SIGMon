from app.repositories.agenda_repository import AgendaRepository
from app.repositories.alocacao_repository import AlocacaoRepository
from app.repositories.sessao_repository import SessaoRepository
from app.utils.validators import BusinessError


class AgendaService:
    def __init__(self):
        self.repo = AgendaRepository()
        self.sessoes = SessaoRepository()
        self.alocacoes = AlocacaoRepository()

    def listar(self, usuario):
        if usuario.papel == "ESTUDANTE":
            return self.repo.list_by_turmas_inscritas(usuario.id_usuario)
        return self.repo.list_all()

    def listar_proprios(self, id_monitor):
        return self.repo.list_by_monitor(id_monitor)

    def listar_inscritos(self, id_usuario):
        return self.repo.list_by_turmas_inscritas(id_usuario)

    def disponiveis(self):
        return self.repo.list_disponiveis()

    def criar_slot(self, data):
        payload = dict(data)
        payload["id_alocacao"] = int(payload["id_alocacao"])
        payload["reservado"] = False
        return self.repo.create(payload)

    def reservar(self, slot_id, estudante, data):
        slot = self.repo.get_by_id(slot_id)
        if not slot:
            raise BusinessError("Horário não encontrado.")
        sessoes_do_slot = [s for s in self.sessoes.list_all() if s.id_slot == slot.id_slot]
        if any(s.id_estudante == estudante.id_usuario for s in sessoes_do_slot):
            raise BusinessError("Voce ja reservou este horario.")
        if slot.reservado and slot.modalidade != "ONLINE":
            raise BusinessError("Este horário já está reservado.")
        alocacao = self.alocacoes.get_by_id(slot.id_alocacao)
        if alocacao and estudante.papel == "MONITOR" and alocacao.id_monitor == estudante.id_usuario:
            raise BusinessError("Monitor nao pode reservar o proprio horario de atendimento.")
        slot.reservado = True
        return self.sessoes.create(
            {
                "id_slot": slot.id_slot,
                "id_estudante": estudante.id_usuario,
                "assunto": data.get("assunto") or "Atendimento de monitoria",
                "observacoes": data.get("observacoes") or "",
                "realizada": False,
                "data_registro": slot.data_slot,
            }
        )
