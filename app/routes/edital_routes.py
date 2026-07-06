from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.departamento_repository import DepartamentoRepository
from app.repositories.edital_repository import EditalRepository
from app.repositories.turma_repository import TurmaRepository
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
    usuario = current_user()
    edital = EditalRepository().get_by_id(id)
    aberto = EditalService().esta_aberto(edital)
    turmas_elegiveis = []
    tem_disciplinas_elegiveis = False
    if usuario.papel in ("ESTUDANTE", "MONITOR") and aberto:
        repo = TurmaRepository()
        turmas_elegiveis = repo.list_elegiveis_para_edital(
            edital.id_departamento, edital.semestre, usuario.id_usuario, edital.nota_minima
        )
        tem_disciplinas_elegiveis = repo.tem_historico_elegivel(
            edital.id_departamento, usuario.id_usuario, edital.nota_minima
        )
    return render_template("editais/detail.html", edital=edital, aberto=aberto,
                           turmas_elegiveis=turmas_elegiveis, tem_disciplinas_elegiveis=tem_disciplinas_elegiveis)


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
@roles_required("ESTUDANTE", "MONITOR")
def candidatar(id):
    try:
        CandidaturaService().candidatar(id, current_user(), request.form)
        flash("Candidatura registrada com sucesso.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("editais.detail", id=id))
