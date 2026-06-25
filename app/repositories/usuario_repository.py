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
    
    def find_by_matricula(self, matricula, excluir_id=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            if excluir_id:
                cursor.execute(
                  "SELECT * FROM usuarios WHERE matricula = %s AND id_usuario != %s",
                  (matricula, excluir_id)
              )
            else:
                cursor.execute("SELECT * FROM usuarios WHERE matricula = %s", (matricula,))
            row = cursor.fetchone()
            return Usuario(*row) if row else None
    
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
      
    def list_by_papel(self, papel):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE papel = %s", 
                             (papel, ))
            rows = cursor.fetchall()
            return [Usuario(*row) for row in rows]
              
    def update(self, usuario_id, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE usuarios
                SET id_departamento=%s, nome=%s, email=%s,
                matricula=%s, papel=%s, senha_hash=%s, ativo=%s
                WHERE id_usuario=%s
                RETURNING *""",
                (
                  payload["id_departamento"],
                  payload["nome"],
                  payload["email"],
                  payload["matricula"],
                  payload["papel"],
                  payload["senha_hash"],
                  payload["ativo"],
                  usuario_id
              )
            )
            conn.commit()
            row = cursor.fetchone()
            return Usuario(*row)
    
    def tem_turmas_ativas(self, id_professor):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM turmas WHERE id_professor = %s", (id_professor,))
            return cursor.fetchone()[0] > 0

    def tem_alocacoes_ativas(self, id_monitor):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM alocacoes_monitores WHERE id_monitor = %s AND status = 'ATIVA'",
                (id_monitor,)
            )
            return cursor.fetchone()[0] > 0

    def tem_turmas_outro_departamento(self, id_professor, id_departamento):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT COUNT(*) FROM turmas t
                   JOIN disciplinas d ON t.id_disciplina = d.id_disciplina
                   WHERE t.id_professor = %s AND d.id_departamento != %s""",
                (id_professor, id_departamento)
            )
            return cursor.fetchone()[0] > 0

    def muda_status(self, usuario_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET ativo = NOT ativo WHERE id_usuario = %s RETURNING *", (usuario_id,))
            conn.commit()
            row = cursor.fetchone()
            return Usuario(*row)