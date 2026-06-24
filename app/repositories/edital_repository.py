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