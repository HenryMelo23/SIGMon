from app.database.db import get_connection
from app.models.sessao_tutoria import SessaoTutoria


class SessaoRepository:
    def count_nao_realizadas(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sessoes_tutoria WHERE realizada = FALSE")
            return cursor.fetchone()[0]
        