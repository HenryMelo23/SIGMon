from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.departamento_repository import DepartamentoRepository
from app.services.disciplina_service import DisciplinaService
from app.utils.decorators import login_required, roles_required
from app.utils.validators import BusinessError

disciplinas_bp = Blueprint("disciplinas", __name__, url_prefix="/disciplinas")


@disciplinas_bp.get("")
@login_required
@roles_required("ADMINISTRADOR")
def index():
    return render_template("disciplinas/list.html", disciplinas=DisciplinaService().listar())


@disciplinas_bp.route("/novo", methods=["GET", "POST"])
@disciplinas_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
@roles_required("ADMINISTRADOR")
def form(id=None):
    service = DisciplinaService()
    if request.method == "POST":
        try:
            service.salvar(request.form, id)
            flash("Disciplina salva.", "success")
            return redirect(url_for("disciplinas.index"))
        except BusinessError as exc:
            flash(str(exc), "danger")
    return render_template("disciplinas/form.html", disciplina=service.obter(id) if id else None, departamentos=DepartamentoRepository().list_all())


@disciplinas_bp.post("/<int:id>/remover")
@login_required
@roles_required("ADMINISTRADOR")
def remover(id):
    try:
        DisciplinaService().remover(id)
        flash("Disciplina removida.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("disciplinas.index"))
