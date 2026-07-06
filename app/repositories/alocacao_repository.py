from app.database.db import get_connection
from app.models.alocacao import AlocacaoMonitor


class AlocacaoRepository:
    def _from_row(self, row):
        return AlocacaoMonitor(*row) if row else None

    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alocacoes_monitores ORDER BY id_alocacao")
            return [AlocacaoMonitor(*row) for row in cursor.fetchall()]

    def get_by_id(self, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alocacoes_monitores WHERE id_alocacao= %s", (id,))
            return self._from_row(cursor.fetchone())

    def list_by_monitor(self, id_monitor):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM alocacoes_monitores
                   WHERE id_monitor = %s AND status = 'ATIVA'
                   ORDER BY data_inicio DESC""",
                (id_monitor,),
            )
            return [AlocacaoMonitor(*row) for row in cursor.fetchall()]

    def list_by_professor(self, id_professor):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM alocacoes_monitores
                   WHERE id_professor = %s
                   ORDER BY data_inicio DESC""",
                (id_professor,),
            )
            return [AlocacaoMonitor(*row) for row in cursor.fetchall()]
    
    def count_ativos(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM alocacoes_monitores WHERE status = 'ATIVA'")
            return cursor.fetchone()[0]
