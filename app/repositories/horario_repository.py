from app.database.db import get_connection
from app.models.horario import Horario


class HorarioRepository:
    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM horarios ORDER BY turno, codigo")
            rows = cursor.fetchall()
            return [Horario(*row) for row in rows]

    def get_by_id(self, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM horarios WHERE id_horario = %s", (id,))
            row = cursor.fetchone()
            return Horario(*row) if row else None

    def find_by_codigo(self, codigo):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM horarios WHERE UPPER(codigo) = UPPER(%s)", (codigo,))
            row = cursor.fetchone()
            return Horario(*row) if row else None

    def create(self, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO horarios (codigo, descricao, turno, ativo)
                   VALUES (%s, %s, %s, %s)
                   RETURNING *""",
                (
                    payload["codigo"],
                    payload["descricao"],
                    payload["turno"],
                    payload["ativo"],
                )
            )
            conn.commit()
            row = cursor.fetchone()
            return Horario(*row)

    def update(self, id_horario, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE horarios
                   SET codigo=%s, descricao=%s, turno=%s, ativo=%s
                   WHERE id_horario=%s
                   RETURNING *""",
                (
                    payload["codigo"],
                    payload["descricao"],
                    payload["turno"],
                    payload["ativo"],
                    id_horario,
                )
            )
            conn.commit()
            row = cursor.fetchone()
            return Horario(*row)

    def delete(self, id_horario):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM horarios WHERE id_horario = %s", (id_horario,))
            conn.commit()
