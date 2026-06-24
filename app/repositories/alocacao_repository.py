from app.database.db import get_connection
from app.models.alocacao import AlocacaoMonitor


class AlocacaoRepository:
    def get_by_id(self, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alocacoes_monitores WHERE id_alocacao= %s", (id,))
            row = cursor.fetchone()
            if row:
                return AlocacaoMonitor(*row)
            return None
    
    def count_ativos(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM alocacoes_monitores WHERE status = 'ATIVA'")
            return cursor.fetchone()[0]