from datetime import date

from app.repositories.alocacao_repository import AlocacaoRepository
from app.repositories.frequencia_repository import FrequenciaRepository
from app.utils.audit import registrar_auditoria
from app.utils.validators import BusinessError


class FrequenciaService:
    def __init__(self):
        self.repo = FrequenciaRepository()

    def listar(self, usuario):
        registros = self.repo.list_all()
        if usuario.papel == "FINANCEIRO":
            return self.repo.list_validadas()
        if usuario.papel == "MONITOR":
            alocacoes = AlocacaoRepository().list_by_monitor(usuario.id_usuario)
            ids = {a.id_alocacao for a in alocacoes}
            return [r for r in registros if r.id_alocacao in ids]
        return registros

    def criar(self, data):
        return self.repo.create(
            {
                "id_alocacao": int(data["id_alocacao"]),
                "data_atividade": data.get("data_atividade") or date.today().isoformat(),
                "horas": float(data["horas"]),
                "descricao": data["descricao"],
                "validado": False,
                "id_professor_validador": None,
            }
        )

    def validar(self, frequencia_id, usuario):
        if usuario.papel != "PROFESSOR":
            raise BusinessError("Apenas professor pode validar frequência.")
        registro = self.repo.update(frequencia_id, {"validado": True, "id_professor_validador": usuario.id_usuario})
        registrar_auditoria(usuario.id_usuario, "VALIDAR_FREQUENCIA", "RegistroFrequencia", f"frequencia_id={frequencia_id}")
        return registro
