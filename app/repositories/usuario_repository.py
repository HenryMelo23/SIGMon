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
    
    def find_by_matricula(self, matricula):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE matricula = %s", (matricula,))
            row = cursor.fetchone()
            if row:
                return Usuario(*row)
            return None
    
    def create(self, payload):
      with get_connection() as conn:
          cursor = conn.cursor()
          cursor.execute(
              """INSERT INTO usuarios (id_departamento, nome,
                 email, matricula, papel, senha_hash, ativo, data_cadastro)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                 RETURNING *""",
              (
                  payload["id_departamento"],
                  payload["nome"],
                  payload["email"],
                  payload["matricula"],
                  payload["papel"],
                  payload["senha_hash"],
                  payload["ativo"],
                  payload["data_cadastro"],
              )
          )
          conn.commit()
          row = cursor.fetchone()
          return Usuario(*row)