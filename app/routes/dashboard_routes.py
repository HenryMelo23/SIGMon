from flask import Blueprint, render_template

from app.repositories.agenda_repository import AgendaRepository
from app.repositories.alocacao_repository import AlocacaoRepository
from app.repositories.avaliacao_repository import AvaliacaoRepository
from app.repositories.candidatura_repository import CandidaturaRepository
from app.repositories.edital_repository import EditalRepository
from app.repositories.frequencia_repository import FrequenciaRepository
from app.repositories.sessao_repository import SessaoRepository
from app.services.edital_service import EditalService
from app.utils.decorators import current_user, login_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.get("")
@login_required
def index():
    usuario = current_user()
    editais = EditalRepository().list_all()
    candidaturas = CandidaturaRepository().list_all()
    sessoes = SessaoRepository().list_all()
    frequencias = FrequenciaRepository().list_all()
    avaliacoes = AvaliacaoRepository().list_all()
    stats = [
        {
            "label": "Editais abertos",
            "value": sum(1 for e in editais if EditalService().esta_aberto(e)),
            "description": "Processos seletivos disponíveis",
            "icon": "◇",
            "endpoint": "editais.index",
            "action_label": "Ver editais",
        },
        {
            "label": "Candidaturas pendentes",
            "value": sum(1 for c in candidaturas if c.status in {"INSCRITA", "EM_ANALISE"}),
            "description": "Aguardando análise acadêmica",
            "icon": "◌",
            "endpoint": "candidaturas.index" if usuario.papel in {"PROFESSOR", "ADMINISTRADOR"} else None,
            "action_label": "Analisar",
        },
        {
            "label": "Monitores ativos",
            "value": sum(1 for a in AlocacaoRepository().list_all() if a.status == "ATIVA"),
            "description": "Alocações em andamento",
            "icon": "▰",
            "endpoint": "alocacoes.index" if usuario.papel in {"MONITOR", "PROFESSOR", "ADMINISTRADOR"} else None,
            "action_label": "Ver alocações",
        },
        {
            "label": "Sessões agendadas",
            "value": sum(1 for s in sessoes if not s.realizada),
            "description": "Atendimentos a realizar",
            "icon": "◍",
            "endpoint": "sessoes.index" if usuario.papel in {"ESTUDANTE", "MONITOR", "PROFESSOR", "ADMINISTRADOR"} else None,
            "action_label": "Ver sessões",
        },
        {
            "label": "Frequências pendentes",
            "value": sum(1 for f in frequencias if not f.validado),
            "description": "Registros aguardando validação",
            "icon": "✓",
            "endpoint": "frequencias.index" if usuario.papel in {"MONITOR", "PROFESSOR", "FINANCEIRO", "ADMINISTRADOR"} else None,
            "action_label": "Ver registros",
        },
        {
            "label": "Avaliações recebidas",
            "value": len(avaliacoes),
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
            ("Registrar frequência", "frequencias.nova", "Enviar atividade realizada"),
            ("Ver avaliações", "avaliacoes.index", "Acompanhar feedbacks recebidos"),
        ],
        "PROFESSOR": [
            ("Analisar candidaturas", "candidaturas.index", "Atualizar status dos estudantes"),
            ("Validar frequências", "frequencias.index", "Conferir atividades de monitores"),
            ("Ver turmas", "turmas.index", "Acompanhar turmas vinculadas"),
        ],
        "ADMINISTRADOR": [
            ("Novo edital", "editais.form", "Publicar processo de monitoria"),
            ("Gerenciar usuários", "usuarios.index", "Manter perfis e permissões"),
            ("Criar disciplina", "disciplinas.form", "Atualizar catálogo do CIC"),
        ],
        "FINANCEIRO": [
            ("Ver monitores ativos", "financeiro.index", "Consultar dados para pagamento"),
            ("Frequências validadas", "frequencias.index", "Conferir registros aprovados"),
        ],
    }
    return render_template(
        "dashboard.html",
        stats=stats,
        quick_actions=quick_actions.get(usuario.papel, []),
        slots=AgendaRepository().list_all(),
        usuario=usuario,
    )
