from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.candidatura_repository import CandidaturaRepository
from app.services.candidatura_service import CandidaturaService
from app.utils.decorators import current_user, login_required, roles_required
from app.utils.validators import BusinessError

candidaturas_bp = Blueprint("candidaturas", __name__)

STATUSES = ["INSCRITA", "EM_ANALISE", "APROVADA", "REPROVADA", "CANCELADA"]


@candidaturas_bp.get("/candidaturas")
@login_required
@roles_required("PROFESSOR", "ADMINISTRADOR")
def index():
    semestre = request.args.get("semestre") or None
    status = request.args.get("status") or None
    semestres = CandidaturaRepository().list_semestres()
    candidaturas = CandidaturaService().listar(current_user(), semestre=semestre, status=status)
    return render_template(
        "candidaturas/list.html",
        candidaturas=candidaturas,
        semestres=semestres,
        semestre_sel=semestre,
        status_sel=status,
        statuses=STATUSES,
    )


@candidaturas_bp.get("/minhas-candidaturas")
@login_required
@roles_required("ESTUDANTE", "MONITOR")
def minhas():
    semestre = request.args.get("semestre") or None
    semestres = CandidaturaRepository().list_semestres()
    candidaturas = CandidaturaService().listar(current_user(), semestre=semestre)
    return render_template(
        "candidaturas/minhas.html",
        candidaturas=candidaturas,
        semestres=semestres,
        semestre_sel=semestre,
    )


@candidaturas_bp.post("/candidaturas/<int:id>/status")
@login_required
@roles_required("PROFESSOR", "ADMINISTRADOR")
def status(id):
    try:
        CandidaturaService().alterar_status(id, request.form["status"], current_user())
        flash("Status da candidatura atualizado.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("candidaturas.index"))


@candidaturas_bp.post("/candidaturas/<int:id>/cancelar")
@login_required
@roles_required("ESTUDANTE", "MONITOR")
def cancelar(id):
    try:
        CandidaturaService().cancelar(id, current_user())
        flash("Candidatura cancelada.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("candidaturas.minhas"))
