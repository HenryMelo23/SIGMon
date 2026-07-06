from app.database.db import get_connection
from app.models.disciplina import Disciplina


class DisciplinaRepository:
    def get_by_id(self, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM disciplinas WHERE id_disciplina= %s", (id,))
            row = cursor.fetchone()
            if row:
                return Disciplina(*row)
            return None
    
    def find_by_codigo(self, codigo):
        with get_connection() as conn:
          cursor = conn.cursor()
          cursor.execute("SELECT * FROM disciplinas WHERE LOWER(codigo) = LOWER(%s)", (codigo,))
          row = cursor.fetchone()
          return Disciplina(*row) if row else None
      
    def tem_turmas(self, id_disciplina):
        with get_connection() as conn:
          cursor = conn.cursor()
          cursor.execute("SELECT COUNT(*) FROM turmas WHERE id_disciplina = %s", (id_disciplina,))
          return cursor.fetchone()[0] > 0
    
    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT d.*, dep.sigla AS departamento_sigla
                FROM disciplinas d
                JOIN departamentos dep ON d.id_departamento =
                dep.id_departamento""")
            rows = cursor.fetchall()
            return [Disciplina(*row) for row in rows]

    def create(self, payload):
      with get_connection() as conn:
          cursor = conn.cursor()
          cursor.execute(
              """INSERT INTO disciplinas (id_departamento, codigo, nome, creditos)
                 VALUES (%s, %s, %s, %s)
                 RETURNING *""",
              (
                  payload["id_departamento"],
                  payload["codigo"],
                  payload["nome"],
                  payload["creditos"]
              )
          )
          conn.commit()
          row = cursor.fetchone()
          return Disciplina(*row)
      
    def update(self, id_disciplina, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE disciplinas
                SET id_departamento=%s, codigo=%s, nome=%s, creditos=%s
                WHERE id_disciplina=%s
                RETURNING *
                """,
                (
                    payload["id_departamento"],
                    payload["codigo"],
                    payload["nome"],
                    payload["creditos"],
                    id_disciplina
                )
            )
            conn.commit()
            row = cursor.fetchone()
            return Disciplina(*row)

    def delete(self, id_disicplina):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM disciplinas WHERE id_disciplina=%s", (id_disicplina,))
            conn.commit()