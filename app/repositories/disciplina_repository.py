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