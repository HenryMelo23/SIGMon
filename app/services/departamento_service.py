from app.repositories.departamento_repository import DepartamentoRepository
from app.utils.validators import BusinessError


class DepartamentoService:
    def __init__(self):
        self.repo = DepartamentoRepository()
    
    def listar(self):
        return self.repo.list_all()

    def obter(self, id):
        return self.repo.get_by_id(id)

    def salvar(self, data, departamento_id=None):
        sigla = data.get("sigla", "").strip().upper()
        nome = data.get("nome", "").strip()
        sigla_existente = self.repo.find_by_sigla(sigla)
        nome_existente = self.repo.find_by_nome(nome)
        if sigla_existente and sigla_existente.id_departamento != (int(departamento_id) if departamento_id else None):
            raise BusinessError("Já existe um departamento com esta sigla.")
        if nome_existente and nome_existente.id_departamento != (int(departamento_id) if departamento_id else None):
            raise BusinessError("Já existe um departamento com este nome.")
        payload = {
              "nome": data.get("nome", "").strip(),
              "sigla": sigla,
              "email": data.get("email", "").strip().lower(),
          }
        return self.repo.update(departamento_id, payload) if departamento_id else self.repo.create(payload)

    def remover(self, id):
        if self.repo.tem_disciplinas(id):
            raise BusinessError("Não é possível remover um departamento que possui disciplinas vinculadas.")
        return self.repo.delete(id)
