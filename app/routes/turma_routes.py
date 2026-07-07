from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.disciplina_repository import DisciplinaRepository
from app.repositories.horario_repository import HorarioRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.turma_repository import TurmaRepository
from app.services.turma_service import TurmaService
from app.utils.decorators import current_user, login_required, roles_required
from app.utils.validators import BusinessError

turmas_bp = Blueprint("turmas", __name__, url_prefix="/turmas")


@turmas_bp.get("")
@login_required
@roles_required("PROFESSOR", "ADMINISTRADOR")
def index():
    usuario = current_user()
    semestre = request.args.get("semestre")
    service = TurmaService()
    if usuario.papel == "PROFESSOR":
        turmas = service.listar_por_professor(usuario.id_usuario, semestre)
    else:
        turmas = service.listar(semestre)
    semestres = TurmaRepository().list_semestres()
    return render_template("turmas/list.html", turmas=turmas, semestre=semestre, semestres=semestres)


@turmas_bp.route("/novo", methods=["GET", "POST"])
@turmas_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
@roles_required("ADMINISTRADOR")
def form(id=None):
    service = TurmaService()
    if request.method == "POST":
        try:
            service.salvar(request.form, id)
            flash("Turma salva.", "success")
            return redirect(url_for("turmas.index"))
        except BusinessError as exc:
            flash(str(exc), "danger")
    return render_template(
        "turmas/form.html",
        turma=service.obter(id) if id else None,
        disciplinas=DisciplinaRepository().list_all(),
        professores=UsuarioRepository().list_by_papel("PROFESSOR"),
        horarios=HorarioRepository().list_ativos(),
    )


@turmas_bp.post("/<int:id>/remover")
@login_required
@roles_required("ADMINISTRADOR")
def remover(id):
    try:
        TurmaService().remover(id)
        flash("Turma removida.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("turmas.index"))
