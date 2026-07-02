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
        if payload.get("hora_fim", "") <= payload.get("hora_inicio", ""):
            raise BusinessError("O horário de fim deve ser posterior ao de início.")
        return self.repo.create(payload)

    def editar_slot(self, slot_id, data, monitor):
        slot = self.repo.get_by_id(slot_id)
        if not slot:
            raise BusinessError("Horário não encontrado.")
        if slot.reservado:
            raise BusinessError("Não é possível editar um horário já reservado.")
        alocacao = self.alocacoes.get_by_id(slot.id_alocacao)
        if not alocacao or alocacao.id_monitor != monitor.id_usuario:
            raise BusinessError("Você não tem permissão para editar este horário.")
        payload = dict(data)
        if payload.get("hora_fim", "") <= payload.get("hora_inicio", ""):
            raise BusinessError("O horário de fim deve ser posterior ao de início.")
        self.repo.update(slot_id, payload)

    def excluir_slot(self, slot_id, monitor):
        slot = self.repo.get_by_id(slot_id)
        if not slot:
            raise BusinessError("Horário não encontrado.")
        if slot.reservado:
            raise BusinessError("Não é possível excluir um horário já reservado.")
        alocacao = self.alocacoes.get_by_id(slot.id_alocacao)
        if not alocacao or alocacao.id_monitor != monitor.id_usuario:
            raise BusinessError("Você não tem permissão para excluir este horário.")
        self.repo.delete(slot_id)

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
        self.repo.marcar_reservado(slot_id)
        return self.sessoes.create(
            {
                "id_slot": slot.id_slot,
                "id_estudante": estudante.id_usuario,
                "assunto": data.get("assunto") or "Atendimento de monitoria",
                "realizada": False,
                "data_registro": slot.data_slot,
            }
        )
