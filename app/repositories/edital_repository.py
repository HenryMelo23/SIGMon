from app.database.db import get_connection
from app.models.edital import Edital


class EditalRepository:
    def get_by_id(self, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM editais WHERE id_edital= %s", (id,))
            row = cursor.fetchone()
            if row:
                return Edital(*row)
            return None
        
    def count_abertos(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM editais WHERE data_fim >= CURRENT_DATE")
            return cursor.fetchone()[0]
    
    def list_all(self, id_departamento=None):
      with get_connection() as conn:
          cursor = conn.cursor()
          if id_departamento:
              cursor.execute("SELECT * FROM editais WHERE id_departamento = %s ORDER BY data_inicio DESC",(id_departamento,))
          else:
              cursor.execute("SELECT * FROM editais ORDER BY data_inicio DESC")
          rows = cursor.fetchall()
          return [Edital(*row) for row in rows]
    
    def tem_candidaturas(self, id_edital):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM candidaturas WHERE id_edital = %s", (id_edital,))
            return cursor.fetchone()[0] > 0
    
    def create(self, payload):
      with get_connection() as conn:
          cursor = conn.cursor()
          cursor.execute(
              """INSERT INTO editais (id_departamento, titulo,
                 descricao, semestre, data_inicio, data_fim, nota_minima,
                 data_inicio_monitoria, data_fim_monitoria)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                 RETURNING *""",
              (
                  payload["id_departamento"],
                  payload["titulo"],
                  payload["descricao"],
                  payload["semestre"],
                  payload["data_inicio"],
                  payload["data_fim"],
                  payload["nota_minima"],
                  payload["data_inicio_monitoria"],
                  payload["data_fim_monitoria"],
              )
          )
          conn.commit()
          row = cursor.fetchone()
          return Edital(*row)

    def update(self, id_edital, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE editais
                SET id_departamento=%s, titulo=%s, descricao=%s,
                semestre=%s, data_inicio=%s, data_fim=%s, nota_minima=%s,
                data_inicio_monitoria=%s, data_fim_monitoria=%s
                WHERE id_edital=%s
                RETURNING *""",
                (
                  payload["id_departamento"],
                  payload["titulo"],
                  payload["descricao"],
                  payload["semestre"],
                  payload["data_inicio"],
                  payload["data_fim"],
                  payload["nota_minima"],
                  payload["data_inicio_monitoria"],
                  payload["data_fim_monitoria"],
                  id_edital
              )
            )
            conn.commit()
            row = cursor.fetchone()
            return Edital(*row)
    
    def delete(self, id_edital):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM editais WHERE id_edital=%s", (id_edital,))
            conn.commit()