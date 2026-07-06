from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.turma_repository import TurmaRepository
from app.services.inscricao_turma_service import InscricaoTurmaService
from app.utils.decorators import current_user, login_required, roles_required
from app.utils.validators import BusinessError

inscricoes_turmas_bp = Blueprint("inscricoes_turmas", __name__, url_prefix="/inscricoes-turmas")


@inscricoes_turmas_bp.get("")
@login_required
@roles_required("ESTUDANTE", "MONITOR", "ADMINISTRADOR")
def index():
    usuario = current_user()
    return render_template(
        "inscricoes_turmas/list.html",
        inscricoes=InscricaoTurmaService().listar(usuario),
        turmas=TurmaRepository().list_all(),
    )


@inscricoes_turmas_bp.post("/nova")
@login_required
@roles_required("ESTUDANTE", "MONITOR")
def nova():
    try:
        InscricaoTurmaService().solicitar(current_user(), request.form)
        flash("Inscricao enviada para aprovacao.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("inscricoes_turmas.index"))


@inscricoes_turmas_bp.post("/<int:id>/status")
@login_required
@roles_required("ADMINISTRADOR")
def status(id):
    try:
        InscricaoTurmaService().alterar_status(id, request.form["status"])
        flash("Status da inscricao atualizado.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("inscricoes_turmas.index"))
