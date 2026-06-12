from collections import defaultdict

from app.repositories.alocacao_repository import AlocacaoRepository
from app.repositories.dados_bancarios_repository import DadosBancariosRepository
from app.repositories.financeiro_repository import FinanceiroRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.utils.audit import registrar_auditoria


class FinanceiroService:
    def __init__(self):
        self.repo = FinanceiroRepository()
        self.usuarios = UsuarioRepository()
        self.dados_bancarios_repo = DadosBancariosRepository()

    def painel(self, usuario):
        registrar_auditoria(usuario.id_usuario, "ACESSAR_FINANCEIRO", "Financeiro", "Visão financeira consolidada")
        monitores = self.repo.monitores_ativos()
        dados_por_usuario = {d.id_usuario: d for d in self.repo.dados_bancarios()}
        frequencias = self.repo.frequencias_validadas()
        horas = defaultdict(float)
        horas_por_monitor = defaultdict(float)
        alocacoes = {a.id_alocacao: a for a in AlocacaoRepository().list_all()}
        for registro in frequencias:
            horas[registro.id_alocacao] += float(registro.horas)
            alocacao = alocacoes.get(registro.id_alocacao)
            if alocacao:
                horas_por_monitor[alocacao.id_monitor] += float(registro.horas)
        return {
            "monitores": monitores,
            "dados_por_usuario": dados_por_usuario,
            "frequencias": frequencias,
            "horas_por_alocacao": dict(horas),
            "horas_por_monitor": dict(horas_por_monitor),
        }
