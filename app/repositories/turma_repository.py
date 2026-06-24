from app.database.db import get_connection
from app.models.turma import Turma


class TurmaRepository:
    def get_by_id(self, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM turmas WHERE id_turma= %s", (id,))
            row = cursor.fetchone()
            if row:
                return Turma(*row)
            return None