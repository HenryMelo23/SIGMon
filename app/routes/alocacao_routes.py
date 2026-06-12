from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.candidatura_repository import CandidaturaRepository
from app.repositories.disciplina_repository import DisciplinaRepository
from app.repositories.turma_repository import TurmaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.alocacao_service import AlocacaoService
from app.utils.decorators import current_user, login_required, roles_required
from app.utils.validators import BusinessError

alocacoes_bp = Blueprint("alocacoes", __name__, url_prefix="/alocacoes")


@alocacoes_bp.get("")
@login_required
@roles_required("MONITOR", "PROFESSOR", "ADMINISTRADOR")
def index():
    return render_template("alocacoes/list.html", alocacoes=AlocacaoService().listar(current_user()))


@alocacoes_bp.route("/nova", methods=["GET", "POST"])
@login_required
@roles_required("ADMINISTRADOR")
def nova():
    if request.method == "POST":
        try:
            AlocacaoService().criar(request.form)
            flash("Alocação criada.", "success")
            return redirect(url_for("alocacoes.index"))
        except BusinessError as exc:
            flash(str(exc), "danger")
    candidaturas = [c for c in CandidaturaRepository().list_all() if c.status == "APROVADA"]
    return render_template(
        "alocacoes/form.html",
        candidaturas=candidaturas,
        monitores=UsuarioRepository().list_by_role("MONITOR"),
        professores=UsuarioRepository().list_by_role("PROFESSOR"),
        disciplinas=DisciplinaRepository().list_all(),
        turmas=TurmaRepository().list_all(),
    )


@alocacoes_bp.post("/<int:id>/status")
@login_required
@roles_required("ADMINISTRADOR", "PROFESSOR")
def status(id):
    AlocacaoService().alterar_status(id, request.form["status"])
    flash("Status da alocação atualizado.", "success")
    return redirect(url_for("alocacoes.index"))
