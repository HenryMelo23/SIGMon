from app.models.departamento import Departamento
from app.database.db import get_connection


class DepartamentoRepository:
    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departamentos")
            rows = cursor.fetchall()
            return [Departamento(*row) for row in rows]