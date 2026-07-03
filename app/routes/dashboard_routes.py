from flask import Blueprint, render_template

from app.repositories.agenda_repository import AgendaRepository
from app.repositories.alocacao_repository import AlocacaoRepository
from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.repositories.candidatura_repository import CandidaturaRepository
from app.repositories.edital_repository import EditalRepository
from app.repositories.sessao_repository import SessaoRepository
from app.utils.decorators import current_user, login_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.get("")
@login_required
def index():
    usuario = current_user()
    editais_abertos = EditalRepository().count_abertos()
    candidaturas_pendentes = CandidaturaRepository().count_pendentes()
    alocacoes_ativas = AlocacaoRepository().count_ativos()
    sessoes_agendadas = SessaoRepository().count_nao_realizadas()
    total_avaliacoes = AvaliacaoRepository().count_all()
    stats = [
        {
            "label": "Editais abertos",
            "value": editais_abertos,
            "description": "Processos seletivos disponíveis",
            "icon": "◇",
            "endpoint": "editais.index",
            "action_label": "Ver editais",
        },
        {
            "label": "Candidaturas pendentes",
            "value": candidaturas_pendentes,
            "description": "Aguardando análise acadêmica",
            "icon": "◌",
            "endpoint": "candidaturas.index" if usuario.papel in {"PROFESSOR", "ADMINISTRADOR"} else None,
            "action_label": "Analisar",
        },
        {
            "label": "Monitores ativos",
            "value": alocacoes_ativas,
            "description": "Alocações em andamento",
            "icon": "▰",
            "endpoint": "alocacoes.index" if usuario.papel in {"MONITOR", "PROFESSOR", "ADMINISTRADOR"} else None,
            "action_label": "Ver alocações",
        },
        {
            "label": "Sessões agendadas",
            "value": sessoes_agendadas,
            "description": "Atendimentos a realizar",
            "icon": "◍",
            "endpoint": "sessoes.index" if usuario.papel in {"ESTUDANTE", "MONITOR", "PROFESSOR", "ADMINISTRADOR"} else None,
            "action_label": "Ver sessões",
        },
        {
            "label": "Avaliações recebidas",
            "value": total_avaliacoes,
            "description": "Feedbacks de tutorias",
            "icon": "★",
            "endpoint": "avaliacoes.index" if usuario.papel in {"ESTUDANTE", "MONITOR", "PROFESSOR", "ADMINISTRADOR"} else None,
            "action_label": "Ver avaliações",
        },
    ]
    quick_actions = {
        "ESTUDANTE": [
            ("Ver editais", "editais.index", "Encontrar processos seletivos abertos"),
            ("Minhas candidaturas", "candidaturas.minhas", "Acompanhar status e histórico"),
            ("Agendar tutoria", "agenda.index", "Reservar atendimento disponível"),
        ],
        "MONITOR": [
            ("Criar horário", "agenda.novo", "Abrir agenda de atendimento"),
            ("Ver sessões", "sessoes.index", "Acompanhar atendimentos"),
            ("Ver avaliações", "avaliacoes.index", "Acompanhar feedbacks recebidos"),
        ],
        "PROFESSOR": [
            ("Analisar candidaturas", "candidaturas.index", "Atualizar status dos estudantes"),
            ("Ver turmas", "turmas.index", "Acompanhar turmas vinculadas"),
            ("Ver avaliações", "avaliacoes.index", "Acompanhar feedbacks dos monitores"),
        ],
        "ADMINISTRADOR": [
            ("Novo edital", "editais.form", "Publicar processo de monitoria"),
            ("Gerenciar usuários", "usuarios.index", "Manter perfis e permissões"),
            ("Criar disciplina", "disciplinas.form", "Atualizar catálogo do CIC"),
        ],
    }
    return render_template(
        "dashboard.html",
        stats=stats,
        quick_actions=quick_actions.get(usuario.papel, []),
        slots=AgendaRepository().list_all(),
        usuario=usuario,
    )
