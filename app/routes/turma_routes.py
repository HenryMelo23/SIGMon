from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.disciplina_repository import DisciplinaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.turma_service import TurmaService
from app.utils.decorators import login_required, roles_required

turmas_bp = Blueprint("turmas", __name__, url_prefix="/turmas")


@turmas_bp.get("")
@login_required
@roles_required("PROFESSOR", "ADMINISTRADOR")
def index():
    semestre = request.args.get("semestre")
    turmas = TurmaService().listar()
    if semestre:
        turmas = [t for t in turmas if t.semestre == semestre]
    return render_template("turmas/list.html", turmas=turmas, semestre=semestre)


@turmas_bp.route("/novo", methods=["GET", "POST"])
@turmas_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
@roles_required("ADMINISTRADOR")
def form(id=None):
    service = TurmaService()
    if request.method == "POST":
        service.salvar(request.form, id)
        flash("Turma salva.", "success")
        return redirect(url_for("turmas.index"))
    return render_template("turmas/form.html", turma=service.obter(id) if id else None, disciplinas=DisciplinaRepository().list_all(), professores=UsuarioRepository().list_by_role("PROFESSOR"))


@turmas_bp.post("/<int:id>/remover")
@login_required
@roles_required("ADMINISTRADOR")
def remover(id):
    TurmaService().remover(id)
    flash("Turma removida.", "success")
    return redirect(url_for("turmas.index"))
