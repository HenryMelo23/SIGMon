from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.departamento_repository import DepartamentoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.usuario_service import UsuarioService
from app.utils.decorators import login_required, roles_required
from app.utils.validators import BusinessError

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuarios_bp.get("")
@login_required
@roles_required("ADMINISTRADOR")
def index():
    papel = request.args.get("papel", "ESTUDANTE")
    return render_template("usuarios/list.html", usuarios=UsuarioService().listar(papel), papel=papel)


@usuarios_bp.route("/novo", methods=["GET", "POST"])
@login_required
@roles_required("ADMINISTRADOR")
def novo():
    volta_papel = request.args.get("papel", "ESTUDANTE")
    if request.method == "POST":
        volta_papel = request.form.get("volta_papel", "ESTUDANTE")
        try:
            UsuarioService().salvar(request.form)
            flash("Usuário criado com sucesso.", "success")
            return redirect(url_for("usuarios.index", papel=volta_papel))
        except BusinessError as exc:
            flash(str(exc), "danger")
    return render_template("usuarios/form.html", usuario=None, departamentos=DepartamentoRepository().list_all(), volta_papel=volta_papel)


@usuarios_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
@roles_required("ADMINISTRADOR")
def editar(id):
    volta_papel = request.args.get("papel", "ESTUDANTE")
    service = UsuarioService()
    if request.method == "POST":
        volta_papel = request.form.get("volta_papel", "ESTUDANTE")
        try:
            service.salvar(request.form, id)
            flash("Usuário atualizado.", "success")
            return redirect(url_for("usuarios.index", papel=volta_papel))
        except BusinessError as exc:
            flash(str(exc), "danger")
    return render_template("usuarios/form.html", usuario=UsuarioRepository().get_by_id(id), departamentos=DepartamentoRepository().list_all(), volta_papel=volta_papel)


@usuarios_bp.post("/<int:id>/status")
@login_required
@roles_required("ADMINISTRADOR")
def status(id):
    papel = request.form.get("papel", "ESTUDANTE")
    try:
        UsuarioService().alternar_status(id)
        flash("Status do usuário atualizado.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("usuarios.index", papel=papel))


@usuarios_bp.post("/encerrar-semestre")
@login_required
@roles_required("ADMINISTRADOR")
def encerrar_semestre():
    from app.repositories.alocacao_repository import AlocacaoRepository
    AlocacaoRepository().encerrar_todas_ativas()
    total = UsuarioRepository().reverter_monitores_para_estudante()
    flash(f"Semestre encerrado: {total} monitor(es) revertido(s) para Estudante.", "success")
    return redirect(url_for("usuarios.index", papel="MONITOR"))
