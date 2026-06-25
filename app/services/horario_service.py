from app.repositories.horario_repository import HorarioRepository
from app.utils.validators import BusinessError


class HorarioService:
    def __init__(self):
        self.repo = HorarioRepository()

    def listar(self):
        return self.repo.list_all()

    def obter(self, id):
        return self.repo.get_by_id(id)

    def salvar(self, data, horario_id=None):
        codigo = data.get("codigo", "").strip().upper()
        existente = self.repo.find_by_codigo(codigo)
        if existente and existente.id_horario != (int(horario_id) if horario_id else None):
            raise BusinessError("Já existe um horário com este código.")
        payload = {
            "codigo": codigo,
            "descricao": data.get("descricao", "").strip(),
"turno": data.get("turno", "").strip().upper(),
            "ativo": data.get("ativo") == "on",
        }
        return self.repo.update(horario_id, payload) if horario_id else self.repo.create(payload)

    def remover(self, id):
        return self.repo.delete(id)
