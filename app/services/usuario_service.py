from datetime import date

from app.repositories.usuario_repository import UsuarioRepository
from app.utils.validators import BusinessError


class UsuarioService:
    def __init__(self):
        self.repo = UsuarioRepository()

    def listar(self, papel=None):
        usuarios = self.repo.list_all()
        return [u for u in usuarios if not papel or u.papel == papel]

    def salvar(self, data, usuario_id=None):
        usuario_id_atual = int(usuario_id) if usuario_id else None
        email = data.get("email", "").strip().lower()
        matricula = data.get("matricula", "").strip()
        usuario_existente = self.repo.find_by_email(email)
        if usuario_existente and usuario_existente.id_usuario != usuario_id_atual:
            raise BusinessError("Ja existe um usuario cadastrado com este e-mail.")
        if matricula and self.repo.find_by_matricula(matricula):
            raise BusinessError("Ja existe um usuario cadastrado com esta matricula.")
        payload = {
            "id_departamento": int(data.get("id_departamento", 1)),
            "nome": data.get("nome", ""),
            "email": email,
            "matricula": matricula,
            "papel": data.get("papel", "ESTUDANTE"),
            "senha_hash": data.get("senha_hash") or "123456",
            "ativo": data.get("ativo", "on") == "on",
            "data_cadastro": data.get("data_cadastro") or date.today().isoformat(),
        }
        return self.repo.update(usuario_id, payload) if usuario_id else self.repo.create(payload)

    def cadastrar_publico(self, data):
        payload = dict(data)
        payload["id_departamento"] = 1
        payload["papel"] = "ESTUDANTE"
        payload["ativo"] = "on"
        return self.salvar(payload)

    def alternar_status(self, usuario_id):
        usuario = self.repo.get_by_id(usuario_id)
        if usuario:
            usuario.ativo = not usuario.ativo
        return usuario
