from app.repositories.turma_repository import TurmaRepository
from app.utils.validators import BusinessError
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.disciplina_repository import DisciplinaRepository


class TurmaService:
    def __init__(self):
        self.repo = TurmaRepository()
    
    def listar(self, semestre=None):
        if semestre:
          return self.repo.list_by_semestre(semestre)
        return self.repo.list_all()
    
    def obter(self, id):
        return self.repo.get_by_id(id)
     
    def salvar(self, data, turma_id=None):
        payload = {
            "id_disciplina": int(data.get("id_disciplina")),
            "id_professor": int(data.get("id_professor")),
            "semestre": data.get("semestre", "").strip(),
            "codigo_turma": data.get("codigo_turma", "").strip().upper(),
            "tipo_turma": data.get("tipo_turma", "").strip(),
            "id_horario": int(data.get("id_horario")),
            "sala": data.get("sala", "").strip(),
        }
        professor = UsuarioRepository().get_by_id(payload["id_professor"])
        disciplina = DisciplinaRepository().get_by_id(payload["id_disciplina"])
        if professor.id_departamento != disciplina.id_departamento:
            raise BusinessError("O professor só pode lecionar disciplinas do seu departamento.")
        conflito = self.repo.find_conflito_horario(
            payload["id_professor"],
            payload["semestre"],
            payload["id_horario"]
        )
        if conflito and conflito.id_turma != (int(turma_id) if turma_id else None):
            raise BusinessError("Este professor já possui uma turma neste horário e semestre.")
        duplicata = self.repo.find_duplicata(
            payload["id_professor"],
            payload["id_disciplina"],
            payload["semestre"],
            payload["codigo_turma"]
        )
        if duplicata and duplicata.id_turma != (int(turma_id) if turma_id else None):
            raise BusinessError("Já existe uma turma com esse código para este professor e disciplina no mesmo semestre.")
        return self.repo.update(turma_id, payload) if turma_id else self.repo.create(payload)

    def remover(self, id):
      if self.repo.tem_alocacoes(id):
          raise BusinessError("Não é possível remover uma turma que possui alocações vinculadas.")
      return self.repo.delete(id)