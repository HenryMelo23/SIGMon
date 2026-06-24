from app.models.avaliacao_tutoria import AvaliacaoTutoria
from app.database.db import get_connection

class AvaliacaoRepository:
    def count_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM avaliacoes_tutoria")
            return cursor.fetchone()[0]