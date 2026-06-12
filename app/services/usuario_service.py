from datetime import date

from app.repositories.usuario_repository import UsuarioRepository


class UsuarioService:
    def __init__(self):
        self.repo = UsuarioRepository()

    def listar(self, papel=None):
        usuarios = self.repo.list_all()
        return [u for u in usuarios if not papel or u.papel == papel]

    def salvar(self, data, usuario_id=None):
        payload = {
            "id_departamento": int(data.get("id_departamento", 1)),
            "nome": data.get("nome", ""),
            "email": data.get("email", ""),
            "matricula": data.get("matricula", ""),
            "papel": data.get("papel", "ESTUDANTE"),
            "senha_hash": data.get("senha_hash") or "123456",
            "ativo": data.get("ativo", "on") == "on",
            "data_cadastro": data.get("data_cadastro") or date.today().isoformat(),
        }
        return self.repo.update(usuario_id, payload) if usuario_id else self.repo.create(payload)

    def alternar_status(self, usuario_id):
        usuario = self.repo.get_by_id(usuario_id)
        if usuario:
            usuario.ativo = not usuario.ativo
        return usuario
