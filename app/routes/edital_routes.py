from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.departamento_repository import DepartamentoRepository
from app.repositories.edital_repository import EditalRepository
from app.services.candidatura_service import CandidaturaService
from app.services.edital_service import EditalService
from app.utils.decorators import current_user, login_required, roles_required
from app.utils.validators import BusinessError

editais_bp = Blueprint("editais", __name__, url_prefix="/editais")


@editais_bp.get("")
@login_required
def index():
    filtro = request.args.get("status")
    usuario = current_user()
    service = EditalService()
    dep = usuario.id_departamento if usuario.papel == "PROFESSOR" else None
    editais_status = service.listar_com_status(dep)
    if filtro == "aberto":
        editais_status = [(e, aberto) for e, aberto in editais_status if aberto]
    if filtro == "encerrado":
        editais_status = [(e, aberto) for e, aberto in editais_status if not aberto]
    return render_template("editais/list.html", editais_status=editais_status, filtro=filtro)

@editais_bp.get("/<int:id>")
@login_required
def detail(id):
    edital = EditalRepository().get_by_id(id)
    return render_template("editais/detail.html", edital=edital, aberto=EditalService().esta_aberto(edital))


@editais_bp.route("/novo", methods=["GET", "POST"])
@editais_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
@roles_required("ADMINISTRADOR")
def form(id=None):
    service = EditalService()
    if request.method == "POST":
        try:
            service.salvar(request.form, id)
            flash("Edital salvo.", "success")
            return redirect(url_for("editais.index"))
        except BusinessError as exc:
            flash(str(exc), "danger")
    return render_template("editais/form.html", edital=service.obter(id) if id else None, departamentos=DepartamentoRepository().list_all())


@editais_bp.post("/<int:id>/remover")
@login_required
@roles_required("ADMINISTRADOR")
def remover(id):
    try:
        EditalService().remover(id)
        flash("Edital removido.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("editais.index"))


@editais_bp.post("/<int:id>/candidatar")
@login_required
@roles_required("ESTUDANTE")
def candidatar(id):
    try:
        CandidaturaService().candidatar(id, current_user(), request.form)
        flash("Candidatura registrada com sucesso.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("editais.detail", id=id))
