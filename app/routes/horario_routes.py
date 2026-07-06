from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.horario_service import HorarioService
from app.utils.decorators import login_required, roles_required
from app.utils.validators import BusinessError

horarios_bp = Blueprint("horarios", __name__, url_prefix="/horarios")


@horarios_bp.get("")
@login_required
@roles_required("ADMINISTRADOR")
def index():
    return render_template("horarios/list.html", horarios=HorarioService().listar())


@horarios_bp.route("/novo", methods=["GET", "POST"])
@horarios_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
@roles_required("ADMINISTRADOR")
def form(id=None):
    service = HorarioService()
    if request.method == "POST":
        try:
            service.salvar(request.form, id)
            flash("Horário salvo.", "success")
            return redirect(url_for("horarios.index"))
        except BusinessError as exc:
            flash(str(exc), "danger")
    return render_template("horarios/form.html", horario=service.obter(id) if id else None)


@horarios_bp.post("/<int:id>/remover")
@login_required
@roles_required("ADMINISTRADOR")
def remover(id):
    try:
        HorarioService().remover(id)
        flash("Horário removido.", "success")
    except Exception:
        flash("Não é possível remover um horário vinculado a turmas.", "danger")
    return redirect(url_for("horarios.index"))
