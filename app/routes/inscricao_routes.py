from flask import Blueprint, Response, flash, redirect, render_template, request, url_for

from app.repositories.inscricao_repository import InscricaoRepository
from app.repositories.turma_repository import TurmaRepository
from app.services.inscricao_service import InscricaoService
from app.utils.decorators import current_user, login_required, roles_required
from app.utils.validators import BusinessError

inscricoes_bp = Blueprint("inscricoes", __name__, url_prefix="/inscricoes")


@inscricoes_bp.get("")
@login_required
@roles_required("ESTUDANTE", "MONITOR", "ADMINISTRADOR")
def index():
    filtro = request.args.get("filtro")
    usuario = current_user()
    inscricoes = InscricaoService().listar(usuario, filtro)
    return render_template("inscricoes/list.html", inscricoes=inscricoes, filtro=filtro)


@inscricoes_bp.route("/novo", methods=["GET", "POST"])
@login_required
@roles_required("ESTUDANTE", "MONITOR")
def novo():
    if request.method == "POST":
        try:
            InscricaoService().cadastrar(
                request.form,
                request.files.get("comprovante"),
                current_user().id_usuario,
            )
            flash("Inscrições enviadas. Aguarde aprovação do administrador.", "success")
            return redirect(url_for("inscricoes.index"))
        except BusinessError as exc:
            flash(str(exc), "danger")
    turmas = TurmaRepository().list_all()
    return render_template("inscricoes/form.html", turmas=turmas)


@inscricoes_bp.post("/<int:id>/aprovar")
@login_required
@roles_required("ADMINISTRADOR")
def aprovar(id):
    InscricaoService().aprovar(id)
    flash("Inscrição aprovada.", "success")
    return redirect(url_for("inscricoes.index"))


@inscricoes_bp.post("/<int:id>/rejeitar")
@login_required
@roles_required("ADMINISTRADOR")
def rejeitar(id):
    try:
        InscricaoService().rejeitar(id, request.form.get("justificativa", ""))
        flash("Inscrição rejeitada.", "danger")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("inscricoes.index"))


@inscricoes_bp.get("/<int:id>/comprovante")
@login_required
@roles_required("ESTUDANTE", "MONITOR", "ADMINISTRADOR")
def comprovante(id):
    inscricao = InscricaoRepository().get_by_id(id)
    if not inscricao or not inscricao.id_documento:
        flash("Comprovante não encontrado.", "danger")
        return redirect(url_for("inscricoes.index"))
    pdf = InscricaoRepository().get_documento(inscricao.id_documento)
    if not pdf:
        flash("Arquivo não encontrado.", "danger")
        return redirect(url_for("inscricoes.index"))
    return Response(
        bytes(pdf),
        mimetype="application/pdf",
        headers={"Content-Disposition": f"inline; filename=comprovante_matricula_{id}.pdf"},
    )


@inscricoes_bp.post("/<int:id>/reverter")
@login_required
@roles_required("ADMINISTRADOR")
def reverter(id):
    try:
        InscricaoService().reverter(id, request.form.get("justificativa", ""))
        flash("Inscrição revertida para rejeitada. O estudante poderá corrigir.", "warning")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("inscricoes.index", filtro="aprovada"))


@inscricoes_bp.post("/<int:id>/remover")
@login_required
@roles_required("ESTUDANTE", "MONITOR", "ADMINISTRADOR")
def remover(id):
    try:
        InscricaoService().remover(id, current_user())
        flash("Inscrição removida.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("inscricoes.index"))
