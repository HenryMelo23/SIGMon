from app.routes.agenda_routes import agenda_bp
from app.routes.alocacao_routes import alocacoes_bp
from app.routes.avaliacao_routes import avaliacoes_bp
from app.routes.auth_routes import auth_bp
from app.routes.candidatura_routes import candidaturas_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.departamento_routes import departamentos_bp
from app.routes.disciplina_routes import disciplinas_bp
from app.routes.edital_routes import editais_bp
from app.routes.financeiro_routes import financeiro_bp
from app.routes.frequencia_routes import frequencias_bp
from app.routes.sessao_routes import sessoes_bp
from app.routes.turma_routes import turmas_bp
from app.routes.usuario_routes import usuarios_bp


def register_blueprints(app):
    for bp in [
        auth_bp,
        dashboard_bp,
        usuarios_bp,
        departamentos_bp,
        disciplinas_bp,
        turmas_bp,
        editais_bp,
        candidaturas_bp,
        alocacoes_bp,
        agenda_bp,
        sessoes_bp,
        frequencias_bp,
        avaliacoes_bp,
        financeiro_bp,
    ]:
        app.register_blueprint(bp)
