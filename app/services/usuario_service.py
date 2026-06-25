from datetime import date

from app.repositories.usuario_repository import UsuarioRepository
from app.utils.validators import BusinessError


class UsuarioService:
    def __init__(self):
        self.repo = UsuarioRepository()

    def listar(self, papel=None):
        return self.repo.list_by_papel(papel)

    def salvar(self, data, usuario_id=None):
        usuario_id_atual = int(usuario_id) if usuario_id else None
        email = data.get("email", "").strip().lower()
        matricula = data.get("matricula", "").strip()
        usuario_existente = self.repo.find_by_email(email)
        if usuario_existente and usuario_existente.id_usuario != usuario_id_atual:
            raise BusinessError("Ja existe um usuario cadastrado com este e-mail.")
        if matricula and self.repo.find_by_matricula(matricula, excluir_id=usuario_id_atual):
            raise BusinessError("Ja existe um usuario cadastrado com esta matricula.")
        novo_papel = data.get("papel", "ESTUDANTE")
        novo_departamento = int(data.get("id_departamento", 1))
        usuario_atual = self.repo.get_by_id(usuario_id_atual) if usuario_id_atual else None
        if usuario_atual:
            if usuario_atual.papel == "PROFESSOR":
                if novo_departamento != usuario_atual.id_departamento:
                    if self.repo.tem_turmas_outro_departamento(usuario_id_atual, novo_departamento):
                        raise BusinessError("Não é possível mudar o departamento: professor possui turmas vinculadas a disciplinas do departamento atual.")
                if novo_papel != "PROFESSOR" and self.repo.tem_turmas_ativas(usuario_id_atual):
                    raise BusinessError("Não é possível mudar o papel: professor possui turmas ativas.")
            if usuario_atual.papel == "MONITOR" and novo_papel != "MONITOR":
                if self.repo.tem_alocacoes_ativas(usuario_id_atual):
                    raise BusinessError("Não é possível mudar o papel: monitor possui alocações ativas.")
        payload = {
            "id_departamento": novo_departamento,
            "nome": data.get("nome", ""),
            "email": email,
            "matricula": matricula,
            "papel": novo_papel,
            "senha_hash": data.get("senha_hash") or "123456",
            "ativo": usuario_atual.ativo if usuario_atual else True,
            "data_cadastro": data.get("data_cadastro") or date.today().isoformat(),
        }
        return self.repo.update(usuario_id, payload) if usuario_id else self.repo.create(payload)

    def cadastrar_publico(self, data):
        payload = dict(data)
        payload["papel"] = "ESTUDANTE"
        payload["ativo"] = "on"
        return self.salvar(payload)

    def alternar_status(self, usuario_id):
        usuario = self.repo.get_by_id(usuario_id)
        if usuario and usuario.ativo:
            if usuario.papel == "PROFESSOR" and self.repo.tem_turmas_ativas(usuario_id):
                raise BusinessError("Não é possível desativar: professor possui turmas ativas.")
            if usuario.papel == "MONITOR" and self.repo.tem_alocacoes_ativas(usuario_id):
                raise BusinessError("Não é possível desativar: monitor possui alocações ativas.")
        return self.repo.muda_status(usuario_id)
        