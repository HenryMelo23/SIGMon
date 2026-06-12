from flask import Blueprint, flash, redirect, render_template, url_for

from app.services.sessao_service import SessaoService
from app.utils.decorators import current_user, login_required, roles_required

sessoes_bp = Blueprint("sessoes", __name__, url_prefix="/sessoes")


@sessoes_bp.get("")
@login_required
@roles_required("ESTUDANTE", "MONITOR", "PROFESSOR", "ADMINISTRADOR")
def index():
    return render_template("sessoes/list.html", sessoes=SessaoService().listar(current_user()))


@sessoes_bp.post("/<int:id>/realizar")
@login_required
@roles_required("MONITOR", "PROFESSOR")
def realizar(id):
    SessaoService().marcar_realizada(id)
    flash("Sessão marcada como realizada.", "success")
    return redirect(url_for("sessoes.index"))
