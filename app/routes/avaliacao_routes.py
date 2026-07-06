from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.repositories.sessao_repository import SessaoRepository
from app.services.avaliacao_service import AvaliacaoService
from app.utils.decorators import current_user, login_required, roles_required
from app.utils.validators import BusinessError

avaliacoes_bp = Blueprint("avaliacoes", __name__, url_prefix="/avaliacoes")


@avaliacoes_bp.get("")
@login_required
@roles_required("ESTUDANTE", "MONITOR", "PROFESSOR", "ADMINISTRADOR")
def index():
    service = AvaliacaoService()
    usuario = current_user()
    return render_template(
        "avaliacoes/list.html",
        avaliacoes=service.listar(usuario),
        desempenho=service.desempenho_por_disciplina(usuario),
        sessoes=SessaoRepository().list_all(),
    )


@avaliacoes_bp.route("/nova/<int:id_sessao>", methods=["GET", "POST"])
@login_required
@roles_required("ESTUDANTE")
def nova(id_sessao):
    sessao = SessaoRepository().get_by_id(id_sessao)
    if request.method == "POST":
        try:
            AvaliacaoService().criar(id_sessao, current_user(), request.form)
            flash("Avaliação registrada.", "success")
            return redirect(url_for("avaliacoes.index"))
        except BusinessError as exc:
            flash(str(exc), "danger")
    return render_template("avaliacoes/form.html", sessao=sessao)
