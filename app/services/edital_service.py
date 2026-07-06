from app.repositories.edital_repository import EditalRepository
from datetime import date
from app.utils.validators import BusinessError


class EditalService:
    def __init__(self):
        self.repo = EditalRepository()
    
    def obter(self, id_edital):
        return self.repo.get_by_id(id_edital)
     
    def listar_com_status(self, id_departamento=None):
        return [(edital, self.esta_aberto(edital)) for edital in self.repo.list_all(id_departamento)]
    
    def esta_aberto(self, edital):
        hoje = date.today()
        return edital.data_inicio <= hoje <= edital.data_fim
    
    def salvar(self, data, edital_id=None):
          payload = {
              "id_departamento": int(data.get("id_departamento")),
              "titulo": data.get("titulo", "").strip(),
              "descricao": data.get("descricao", "").strip(),
              "semestre": data.get("semestre", "").strip(),
              "data_inicio": data.get("data_inicio"),
              "data_fim": data.get("data_fim"),
              "nota_minima": data.get("nota_minima", "MS").strip().upper(),
              "data_inicio_monitoria": data.get("data_inicio_monitoria"),
              "data_fim_monitoria": data.get("data_fim_monitoria"),
          }

          data_inicio = date.fromisoformat(payload["data_inicio"])
          data_fim = date.fromisoformat(payload["data_fim"])
          data_inicio_mon = date.fromisoformat(payload["data_inicio_monitoria"])
          data_fim_mon = date.fromisoformat(payload["data_fim_monitoria"])

          if not edital_id and data_inicio < date.today():
              raise BusinessError("A data de início não pode ser no passado.")
          if data_fim < data_inicio:
              raise BusinessError("A data de fim não pode ser anterior à data de início.")
          if data_inicio_mon < data_fim:
              raise BusinessError("A monitoria deve iniciar após o encerramento das inscrições.")
          if data_fim_mon < data_inicio_mon:
              raise BusinessError("A data de fim da monitoria não pode ser anterior ao início.")
          
          return self.repo.update(edital_id, payload) if edital_id else self.repo.create(payload)

    def remover(self, id):
      if self.repo.tem_candidaturas(id):
          raise BusinessError("Não é possível remover um edital que possui candidaturas vinculadas.")
      return self.repo.delete(id)