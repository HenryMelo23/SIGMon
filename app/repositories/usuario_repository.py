from app.database.db import get_connection
from app.models.usuario import Usuario


class UsuarioRepository:
    def find_by_email(self, email):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE LOWER(email) = LOWER(%s)", (email,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Usuario(*row)
    
    def get_by_id(self, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Usuario(*row)
