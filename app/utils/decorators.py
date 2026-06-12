from functools import wraps

from flask import abort, redirect, session, url_for

from app.repositories.usuario_repository import UsuarioRepository


def current_user():
    user_id = session.get("user_id")
    return UsuarioRepository().get_by_id(user_id) if user_id else None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))
        usuario = current_user()
        if not usuario or not usuario.ativo:
            session.clear()
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


def roles_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            usuario = current_user()
            if not usuario or usuario.papel not in roles:
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator
