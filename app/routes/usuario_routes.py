from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.departamento_repository import DepartamentoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.usuario_service import UsuarioService
from app.utils.decorators import login_required, roles_required

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuarios_bp.get("")
@login_required
@roles_required("ADMINISTRADOR")
def index():
    papel = request.args.get("papel")
    return render_template("usuarios/list.html", usuarios=UsuarioService().listar(papel), papel=papel)


@usuarios_bp.route("/novo", methods=["GET", "POST"])
@login_required
@roles_required("ADMINISTRADOR")
def novo():
    if request.method == "POST":
        UsuarioService().salvar(request.form)
        flash("Usuário criado com sucesso.", "success")
        return redirect(url_for("usuarios.index"))
    return render_template("usuarios/form.html", usuario=None, departamentos=DepartamentoRepository().list_all())


@usuarios_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
@roles_required("ADMINISTRADOR")
def editar(id):
    service = UsuarioService()
    if request.method == "POST":
        service.salvar(request.form, id)
        flash("Usuário atualizado.", "success")
        return redirect(url_for("usuarios.index"))
    return render_template("usuarios/form.html", usuario=UsuarioRepository().get_by_id(id), departamentos=DepartamentoRepository().list_all())


@usuarios_bp.post("/<int:id>/status")
@login_required
@roles_required("ADMINISTRADOR")
def status(id):
    UsuarioService().alternar_status(id)
    flash("Status do usuário atualizado.", "success")
    return redirect(url_for("usuarios.index"))
