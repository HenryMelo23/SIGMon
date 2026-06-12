from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.candidatura_service import CandidaturaService
from app.utils.decorators import current_user, login_required, roles_required
from app.utils.validators import BusinessError

candidaturas_bp = Blueprint("candidaturas", __name__)


@candidaturas_bp.get("/candidaturas")
@login_required
@roles_required("PROFESSOR", "ADMINISTRADOR")
def index():
    return render_template("candidaturas/list.html", candidaturas=CandidaturaService().listar(current_user()))


@candidaturas_bp.get("/minhas-candidaturas")
@login_required
@roles_required("ESTUDANTE")
def minhas():
    return render_template("candidaturas/minhas.html", candidaturas=CandidaturaService().listar(current_user()))


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
