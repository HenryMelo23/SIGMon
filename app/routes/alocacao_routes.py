from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.alocacao_service import AlocacaoService
from app.utils.decorators import current_user, login_required, roles_required
from app.utils.validators import BusinessError

alocacoes_bp = Blueprint("alocacoes", __name__, url_prefix="/alocacoes")


@alocacoes_bp.get("")
@login_required
@roles_required("MONITOR", "PROFESSOR", "ADMINISTRADOR")
def index():
    return render_template("alocacoes/list.html", alocacoes=AlocacaoService().listar(current_user()))


@alocacoes_bp.post("/<int:id>/status")
@login_required
@roles_required("ADMINISTRADOR", "PROFESSOR")
def status(id):
    try:
        AlocacaoService().alterar_status(id, request.form["status"])
        flash("Status da alocação atualizado.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("alocacoes.index"))
