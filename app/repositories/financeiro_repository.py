from app.repositories.dados_bancarios_repository import DadosBancariosRepository
from app.repositories.frequencia_repository import FrequenciaRepository
from app.repositories.usuario_repository import UsuarioRepository


class FinanceiroRepository:
    def monitores_ativos(self):
        return [u for u in UsuarioRepository().list_by_role("MONITOR") if u.ativo]

    def dados_bancarios(self):
        return DadosBancariosRepository().list_all()

    def frequencias_validadas(self):
        return FrequenciaRepository().list_validadas()
