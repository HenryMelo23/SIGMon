from app.repositories.disciplina_repository import DisciplinaRepository
from app.utils.validators import BusinessError

class DisciplinaService:
    def __init__(self):
        self.repo = DisciplinaRepository()
    
    def listar(self):
        return self.repo.list_all()
    
    def obter(self, id):
        return self.repo.get_by_id(id)

    def salvar(self, data, id_disciplina=None):
        codigo = data.get("codigo", "").strip().upper()
        codigo_existente = self.repo.find_by_codigo(codigo)
        if codigo_existente and codigo_existente.id_disciplina != (int(id_disciplina) if id_disciplina else None):
            raise BusinessError("Já existe uma disciplina com este código.")
        novo_departamento = data.get("id_departamento", "").strip()
        if id_disciplina:
            disciplina_atual = self.repo.get_by_id(id_disciplina)
            if disciplina_atual and str(disciplina_atual.id_departamento) != str(novo_departamento):
                if self.repo.tem_turmas(id_disciplina):
                    raise BusinessError("Não é possível mudar o departamento de uma disciplina que possui turmas vinculadas.")
        payload = {
              "id_departamento": novo_departamento,
              "codigo": codigo,
              "nome": data.get("nome", "").strip(),
              "creditos": data.get("creditos", "").strip(),
          }
        return self.repo.update(id_disciplina, payload) if id_disciplina else self.repo.create(payload)

    def remover(self, id):
        if self.repo.tem_turmas(id):
          raise BusinessError("Não é possível remover uma disciplina que possui turmas vinculadas.")
        return self.repo.delete(id)