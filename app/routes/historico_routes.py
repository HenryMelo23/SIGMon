from flask import Blueprint, flash, redirect, render_template, request, url_for, Response

from app.repositories.disciplina_repository import DisciplinaRepository
from app.repositories.historico_repository import HistoricoRepository
from app.services.historico_service import HistoricoService
from app.utils.decorators import current_user, login_required, roles_required
from app.utils.validators import BusinessError

historico_bp = Blueprint("historico", __name__, url_prefix="/historico")


@historico_bp.get("")
@login_required
@roles_required("ESTUDANTE", "MONITOR", "ADMINISTRADOR")
def index():
    filtro = request.args.get("filtro")
    usuario = current_user()
    historicos = HistoricoService().listar(usuario, filtro)
    return render_template("historico/list.html", historicos=historicos, filtro=filtro)


@historico_bp.route("/novo", methods=["GET", "POST"])
@login_required
@roles_required("ESTUDANTE", "MONITOR")
def novo():
    if request.method == "POST":
        try:
            HistoricoService().cadastrar(request.form, request.files.get("comprovante"), current_user().id_usuario)
            flash("Histórico enviado. Aguarde aprovação do administrador.", "success")
            return redirect(url_for("historico.index"))
        except BusinessError as exc:
            flash(str(exc), "danger")
    return render_template("historico/form.html", disciplinas=DisciplinaRepository().list_all())


@historico_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
@roles_required("ESTUDANTE", "MONITOR")
def editar(id):
    service = HistoricoService()
    historico = service.obter(id)
    if not historico or historico.status != "REJEITADO":
        flash("Só é possível editar históricos rejeitados.", "danger")
        return redirect(url_for("historico.index"))
    if request.method == "POST":
        try:
            service.editar(id, request.form, request.files.get("comprovante"), current_user())
            flash("Histórico atualizado. Aguarde nova análise.", "success")
            return redirect(url_for("historico.index"))
        except BusinessError as exc:
            flash(str(exc), "danger")
    return render_template("historico/form_editar.html", historico=historico, disciplinas=DisciplinaRepository().list_all())


@historico_bp.post("/<int:id>/aprovar")
@login_required
@roles_required("ADMINISTRADOR")
def aprovar(id):
    HistoricoService().aprovar(id)
    flash("Histórico aprovado.", "success")
    return redirect(url_for("historico.index"))


@historico_bp.post("/<int:id>/rejeitar")
@login_required
@roles_required("ADMINISTRADOR")
def rejeitar(id):
    try:
        HistoricoService().rejeitar(id, request.form.get("justificativa", ""))
        flash("Histórico rejeitado.", "danger")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("historico.index"))


@historico_bp.get("/<int:id>/comprovante")
@login_required
@roles_required("ESTUDANTE", "MONITOR", "ADMINISTRADOR")
def comprovante(id):
    historico = HistoricoRepository().get_by_id(id)
    if not historico or not historico.id_documento:
        flash("Comprovante não encontrado.", "danger")
        return redirect(url_for("historico.index"))
    pdf = HistoricoRepository().get_documento(historico.id_documento)
    if not pdf:
        flash("Arquivo não encontrado.", "danger")
        return redirect(url_for("historico.index"))
    return Response(bytes(pdf), mimetype="application/pdf",
                    headers={"Content-Disposition": f"inline; filename=comprovante_{id}.pdf"})


@historico_bp.post("/<int:id>/reverter")
@login_required
@roles_required("ADMINISTRADOR")
def reverter(id):
    try:
        HistoricoService().reverter(id, request.form.get("justificativa", ""))
        flash("Histórico revertido para rejeitado. O estudante poderá corrigir.", "warning")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("historico.index", filtro="aprovado"))


@historico_bp.post("/<int:id>/remover")
@login_required
@roles_required("ESTUDANTE", "MONITOR", "ADMINISTRADOR")
def remover(id):
    try:
        HistoricoService().remover(id, current_user())
        flash("Histórico removido.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("historico.index"))
