from app.repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository):
    dataset_name = "usuarios"
    id_field = "id_usuario"

    def find_by_email(self, email):
        return next((u for u in self.items if u.email.lower() == email.lower()), None)

    def list_by_role(self, papel):
        return [u for u in self.items if u.papel == papel]
