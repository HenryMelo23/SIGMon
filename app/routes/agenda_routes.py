from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.alocacao_repository import AlocacaoRepository
from app.repositories.sessao_repository import SessaoRepository
from app.services.agenda_service import AgendaService
from app.utils.decorators import current_user, login_required, roles_required
from app.utils.validators import BusinessError

agenda_bp = Blueprint("agenda", __name__, url_prefix="/agenda")


@agenda_bp.get("")
@login_required
@roles_required("ESTUDANTE", "MONITOR", "PROFESSOR", "ADMINISTRADOR")
def index():
    usuario = current_user()
    service = AgendaService()
    if usuario.papel == "MONITOR":
        return render_template(
            "agenda/list.html",
            meus_slots=service.listar_proprios(usuario.id_usuario),
            slots_agenda=service.listar_inscritos(usuario.id_usuario),
        )
    return render_template("agenda/list.html", slots=service.listar(usuario))


@agenda_bp.route("/novo", methods=["GET", "POST"])
@login_required
@roles_required("MONITOR")
def novo():
    if request.method == "POST":
        try:
            AgendaService().criar_slot(request.form)
            flash("Horário de atendimento criado.", "success")
            return redirect(url_for("agenda.index"))
        except BusinessError as exc:
            flash(str(exc), "danger")
    return render_template("agenda/form.html", alocacoes=AlocacaoRepository().list_by_monitor(current_user().id_usuario))


@agenda_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
@roles_required("MONITOR")
def editar(id):
    service = AgendaService()
    slot = service.repo.get_by_id(id)
    if not slot or slot.reservado:
        flash("Horário não encontrado ou já reservado.", "danger")
        return redirect(url_for("agenda.index"))
    if request.method == "POST":
        try:
            service.editar_slot(id, request.form, current_user())
            flash("Horário atualizado.", "success")
            return redirect(url_for("agenda.index"))
        except BusinessError as exc:
            flash(str(exc), "danger")
    return render_template("agenda/form.html",
                           alocacoes=AlocacaoRepository().list_by_monitor(current_user().id_usuario),
                           slot=slot)


@agenda_bp.post("/<int:id>/excluir")
@login_required
@roles_required("MONITOR")
def excluir(id):
    try:
        AgendaService().excluir_slot(id, current_user())
        flash("Horário excluído.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("agenda.index"))


@agenda_bp.post("/<int:id>/reservar")
@login_required
@roles_required("ESTUDANTE", "MONITOR")
def reservar(id):
    try:
        AgendaService().reservar(id, current_user(), request.form)
        flash("Horário reservado e sessão criada.", "success")
    except BusinessError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("agenda.index"))
