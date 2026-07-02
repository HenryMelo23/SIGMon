from flask import Blueprint, flash, redirect, render_template, url_for

from app.repositories.agenda_repository import AgendaRepository
from app.services.sessao_service import SessaoService
from app.utils.decorators import current_user, login_required, roles_required

sessoes_bp = Blueprint("sessoes", __name__, url_prefix="/sessoes")


@sessoes_bp.get("")
@login_required
@roles_required("ESTUDANTE", "MONITOR", "PROFESSOR", "ADMINISTRADOR")
def index():
    usuario = current_user()
    service = SessaoService()
    slots = {slot.id_slot: slot for slot in AgendaRepository().list_all()}
    if usuario.papel == "MONITOR":
        return render_template(
            "sessoes/list.html",
            sessoes_monitor=service.listar_como_monitor(usuario.id_usuario),
            sessoes_estudante=service.listar_como_estudante(usuario.id_usuario),
            slots=slots,
        )
    return render_template("sessoes/list.html", sessoes=service.listar(usuario), slots=slots)


@sessoes_bp.post("/<int:id>/realizar")
@login_required
@roles_required("MONITOR", "PROFESSOR")
def realizar(id):
    SessaoService().marcar_realizada(id)
    flash("Sessão marcada como realizada.", "success")
    return redirect(url_for("sessoes.index"))
