from app.repositories.usuario_repository import UsuarioRepository
from app.utils.validators import BusinessError


class AuthService:
    def __init__(self):
        self.usuarios = UsuarioRepository()

    def login(self, email, senha):
        usuario = self.usuarios.find_by_email(email)
        if not usuario or usuario.senha_hash != senha:
            raise BusinessError("E-mail ou senha inválidos.")
        if not usuario.ativo:
            raise BusinessError("Usuário inativo. Procure a secretaria do departamento.")
        return usuario
