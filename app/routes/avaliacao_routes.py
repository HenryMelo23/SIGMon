from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.agenda_repository import AgendaRepository
from app.repositories.sessao_repository import SessaoRepository
from app.services.avaliacao_service import AvaliacaoService
from app.utils.decorators import current_user, login_required, roles_required
from app.utils.validators import BusinessError

avaliacoes_bp = Blueprint("avaliacoes", __name__, url_prefix="/avaliacoes")


@avaliacoes_bp.get("")
@login_required
@roles_required("ESTUDANTE", "MONITOR", "PROFESSOR", "ADMINISTRADOR")
def index():
    usuario = current_user()
    service = AvaliacaoService()
    if usuario.papel == "MONITOR":
        return render_template(
            "avaliacoes/list.html",
            recebidas=service.listar_recebidas(usuario.id_usuario),
            feitas=service.listar_feitas(usuario.id_usuario),
            resumo=service.resumo_monitor(usuario.id_usuario),
        )
    return render_template("avaliacoes/list.html", avaliacoes=service.listar(usuario))


@avaliacoes_bp.route("/nova/<int:id_sessao>", methods=["GET", "POST"])
@login_required
@roles_required("ESTUDANTE", "MONITOR")
def nova(id_sessao):
    sessao = SessaoRepository().get_by_id(id_sessao)
    if not sessao:
        flash("Sessão não encontrada.", "danger")
        return redirect(url_for("sessoes.index"))
    if request.method == "POST":
        try:
            AvaliacaoService().criar(id_sessao, current_user(), request.form)
            flash("Avaliação registrada.", "success")
            return redirect(url_for("avaliacoes.index"))
        except BusinessError as exc:
            flash(str(exc), "danger")
    slot = AgendaRepository().get_by_id(sessao.id_slot)
    return render_template("avaliacoes/form.html", sessao=sessao, slot=slot)
