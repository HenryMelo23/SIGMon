from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.departamento_service import DepartamentoService
from app.utils.decorators import login_required, roles_required

departamentos_bp = Blueprint("departamentos", __name__, url_prefix="/departamentos")


@departamentos_bp.get("")
@login_required
@roles_required("ADMINISTRADOR")
def index():
    return render_template("departamentos/list.html", departamentos=DepartamentoService().listar())


@departamentos_bp.route("/novo", methods=["GET", "POST"])
@departamentos_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
@roles_required("ADMINISTRADOR")
def form(id=None):
    service = DepartamentoService()
    if request.method == "POST":
        service.salvar(request.form, id)
        flash("Departamento salvo.", "success")
        return redirect(url_for("departamentos.index"))
    return render_template("departamentos/form.html", departamento=service.obter(id) if id else None)


@departamentos_bp.post("/<int:id>/remover")
@login_required
@roles_required("ADMINISTRADOR")
def remover(id):
    DepartamentoService().remover(id)
    flash("Departamento removido.", "success")
    return redirect(url_for("departamentos.index"))
