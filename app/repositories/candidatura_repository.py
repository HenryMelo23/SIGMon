from app.database.db import get_connection
from app.models.candidatura import Candidatura


class CandidaturaRepository:
    def count_pendentes(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM candidaturas WHERE status IN ('INSCRITA', 'EM_ANALISE')")
            return cursor.fetchone()[0]