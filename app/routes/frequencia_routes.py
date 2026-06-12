from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.alocacao_repository import AlocacaoRepository
from app.services.frequencia_service import FrequenciaService
from app.utils.decorators import current_user, login_required, roles_required
from app.utils.validators import BusinessError

frequencias_bp = Blueprint("frequencias", __name__, url_prefix="/frequencias")


@frequencias_bp.get("")
@login_required
@roles_required("MONITOR", "PROFESSOR", "FINANCEIRO", "ADMINISTRADOR")
def index():
    return render_template("frequencias/list.html", frequencias=FrequenciaService().listar(current_user()))


@frequencias_bp.route("/nova", methods=["GET", "POST"])
@login_required
@roles_required("MONITOR")
def nova():
    if request.method == "POST":
        FrequenciaService().criar(request.form)
        flash("Frequência registrada como pendente.", "success")
        return redirect(url_for("frequencias.index"))
    return render_template("frequencias/form.html", alocacoes=AlocacaoRepository().list_by_monitor(current_user().id_usuario))


@frequencias_bp.post("/<int:id>/validar")
@login_required
@roles_required("PROFESSOR")
def validar(id):
    try:
        FrequenciaService().validar(id, current_user())
        flash("Frequência validada.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("frequencias.index"))
