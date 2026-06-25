from app.models.departamento import Departamento
from app.database.db import get_connection


class DepartamentoRepository:
    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departamentos")
            rows = cursor.fetchall()
            return [Departamento(*row) for row in rows]
    
    def get_by_id(self, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departamentos WHERE id_departamento = %s", (id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Departamento(*row)
    
    def find_by_sigla(self, sigla):
      with get_connection() as conn:
          cursor = conn.cursor()
          cursor.execute("SELECT * FROM departamentos WHERE LOWER(sigla) = LOWER(%s)", (sigla,))
          row = cursor.fetchone()
          return Departamento(*row) if row else None
      
    def find_by_nome(self, nome):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departamentos WHERE unaccent(LOWER(nome)) = unaccent(LOWER(%s))", (nome,))
            row = cursor.fetchone()
            return Departamento(*row) if row else None
    
    def create(self, payload):
      with get_connection() as conn:
          cursor = conn.cursor()
          cursor.execute(
              """INSERT INTO departamentos (nome, sigla, email)
                 VALUES (%s, %s, %s)
                 RETURNING *""",
              (
                  payload["nome"],
                  payload["sigla"],
                  payload["email"],
              )
          )
          conn.commit()
          row = cursor.fetchone()
          return Departamento(*row)
      
    def update(self, id_departamento, payload):
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """UPDATE departamentos
                    SET nome=%s, sigla=%s, email=%s
                    WHERE id_departamento=%s
                    RETURNING *""",
                    (
                    payload["nome"],
                    payload["sigla"],
                    payload["email"],
                    id_departamento
                )
                )
                conn.commit()
                row = cursor.fetchone()
                return Departamento(*row)
    
    def tem_disciplinas(self, id_departamento):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM disciplinas WHERE id_departamento = %s", (id_departamento,))
            return cursor.fetchone()[0] > 0

    def delete(self, id_departamento):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM departamentos WHERE id_departamento=%s", (id_departamento,))
            conn.commit()