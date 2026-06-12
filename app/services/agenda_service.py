from app.repositories.agenda_repository import AgendaRepository
from app.repositories.sessao_repository import SessaoRepository
from app.utils.validators import BusinessError


class AgendaService:
    def __init__(self):
        self.repo = AgendaRepository()
        self.sessoes = SessaoRepository()

    def listar(self):
        return self.repo.list_all()

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
        if slot.reservado:
            raise BusinessError("Este horário já está reservado.")
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
