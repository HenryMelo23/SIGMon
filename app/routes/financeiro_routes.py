from flask import Blueprint, render_template

from app.services.financeiro_service import FinanceiroService
from app.utils.decorators import current_user, login_required, roles_required

financeiro_bp = Blueprint("financeiro", __name__, url_prefix="/financeiro")


@financeiro_bp.get("")
@login_required
@roles_required("FINANCEIRO", "ADMINISTRADOR")
def index():
    return render_template("financeiro/index.html", painel=FinanceiroService().painel(current_user()))
