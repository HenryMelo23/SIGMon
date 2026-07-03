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
    papel = usuario.papel
    repo_agenda = AgendaRepository()

    stats = _build_stats(papel, usuario.id_usuario)

    if papel == "ESTUDANTE":
        slots = repo_agenda.list_by_turmas_inscritas(usuario.id_usuario)
    elif papel == "MONITOR":
        slots = repo_agenda.list_para_monitor(usuario.id_usuario)
    elif papel == "PROFESSOR":
        slots = repo_agenda.list_by_professor(usuario.id_usuario)
    else:
        slots = repo_agenda.list_all()

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
        quick_actions=quick_actions.get(papel, []),
        slots=slots,
        usuario=usuario,
    )


def _build_stats(papel, id_usuario=None):
    editais_abertos     = EditalRepository().count_abertos()
    candidaturas_pend   = CandidaturaRepository().count_pendentes()
    alocacoes_ativas    = AlocacaoRepository().count_ativos()
    sessoes_agendadas   = SessaoRepository().count_nao_realizadas()
    repo_av = AvaliacaoRepository()
    if papel == "MONITOR" and id_usuario:
        total_avaliacoes = repo_av.count_recebidas_monitor(id_usuario)
    else:
        total_avaliacoes = repo_av.count_all()

    all_stats = {
        "editais": {
            "label": "Editais abertos",
            "value": editais_abertos,
            "description": "Processos seletivos disponíveis",
            "icon": "◇",
            "endpoint": "editais.index",
            "action_label": "Ver editais",
        },
        "candidaturas": {
            "label": "Candidaturas pendentes",
            "value": candidaturas_pend,
            "description": "Aguardando análise acadêmica",
            "icon": "◌",
            "endpoint": "candidaturas.index",
            "action_label": "Analisar",
        },
        "alocacoes": {
            "label": "Monitores ativos",
            "value": alocacoes_ativas,
            "description": "Alocações em andamento",
            "icon": "▰",
            "endpoint": "alocacoes.index",
            "action_label": "Ver alocações",
        },
        "sessoes": {
            "label": "Sessões agendadas",
            "value": sessoes_agendadas,
            "description": "Atendimentos a realizar",
            "icon": "◍",
            "endpoint": "sessoes.index",
            "action_label": "Ver sessões",
        },
        "avaliacoes": {
            "label": "Avaliações recebidas",
            "value": total_avaliacoes,
            "description": "Feedbacks de tutorias",
            "icon": "★",
            "endpoint": "avaliacoes.index",
            "action_label": "Ver avaliações",
        },
    }

    ordem = {
        "ESTUDANTE":     ["editais", "sessoes"],
        "MONITOR":       ["editais", "sessoes", "avaliacoes"],
        "PROFESSOR":     ["candidaturas", "alocacoes", "sessoes", "avaliacoes"],
        "ADMINISTRADOR": ["editais", "candidaturas", "alocacoes", "sessoes", "avaliacoes"],
    }

    return [all_stats[k] for k in ordem.get(papel, [])]
