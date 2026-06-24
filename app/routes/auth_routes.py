from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from app.services.auth_service import AuthService
from app.services.usuario_service import UsuarioService
from app.utils.validators import BusinessError

auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/login")
def login():
    if session.get("user_id"):
        return redirect(url_for("dashboard.index"))
    return render_template("login.html")


@auth_bp.post("/login")
def do_login():
    try:
        usuario = AuthService().login(request.form.get("email", ""), request.form.get("senha", ""))
        session["user_id"] = usuario.id_usuario
        flash(f"Bem-vindo(a), {usuario.nome}.", "success")
        return redirect(url_for("dashboard.index"))
    except BusinessError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("auth.login"))


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if session.get("user_id"):
        return redirect(url_for("dashboard.index"))
    if request.method == "POST":
        try:
            usuario = UsuarioService().cadastrar_publico(request.form)
            session["user_id"] = usuario.id_usuario
            flash("Cadastro criado. Voce ja esta conectado ao SIGMon.", "success")
            return redirect(url_for("dashboard.index"))
        except BusinessError as exc:
            flash(str(exc), "danger")
    return render_template("cadastro.html")


@auth_bp.get("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada com segurança.", "info")
    return redirect(url_for("auth.login"))
