from flask import Flask, redirect, render_template, session, url_for

from app.config import Config
from app.routes import register_blueprints
from app.repositories.alocacao_repository import AlocacaoRepository
from app.repositories.disciplina_repository import DisciplinaRepository
from app.repositories.edital_repository import EditalRepository
from app.repositories.turma_repository import TurmaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.utils.permissions import ROLE_LABELS, menu_for_role


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    register_blueprints(app)

    @app.context_processor
    def inject_current_user():
        user_id = session.get("user_id")
        usuario = UsuarioRepository().get_by_id(user_id) if user_id else None
        usuarios = UsuarioRepository()
        disciplinas = DisciplinaRepository()
        turmas = TurmaRepository()
        editais = EditalRepository()
        alocacoes = AlocacaoRepository()
        return {
            "current_user": usuario,
            "role_labels": ROLE_LABELS,
            "menu_items": menu_for_role(usuario.papel) if usuario else [],
            "get_usuario": usuarios.get_by_id,
            "get_disciplina": disciplinas.get_by_id,
            "get_turma": turmas.get_by_id,
            "get_edital": editais.get_by_id,
            "get_alocacao": alocacoes.get_by_id,
        }

    @app.route("/")
    def index():
        if session.get("user_id"):
            return redirect(url_for("dashboard.index"))
        return redirect(url_for("auth.login"))

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(_error):
        return render_template("errors/500.html"), 500

    return app
