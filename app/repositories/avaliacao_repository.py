from app.models.avaliacao_tutoria import AvaliacaoTutoria
from app.database.db import get_connection

class AvaliacaoRepository:
    def _from_row(self, row):
        return AvaliacaoTutoria(*row) if row else None

    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM avaliacoes_tutoria ORDER BY data_avaliacao DESC, id_avaliacao DESC")
            return [AvaliacaoTutoria(*row) for row in cursor.fetchall()]

    def create(self, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO avaliacoes_tutoria
                   (id_sessao, id_estudante, nota, comentario, data_avaliacao)
                   VALUES (%s, %s, %s, %s, %s)
                   RETURNING *""",
                (
                    payload["id_sessao"],
                    payload["id_estudante"],
                    payload["nota"],
                    payload["comentario"],
                    payload["data_avaliacao"],
                ),
            )
            conn.commit()
            return self._from_row(cursor.fetchone())

    def desempenho_por_disciplina(self, id_monitor=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            if id_monitor:
                cursor.execute(
                    """SELECT monitor, disciplina, media_nota, total_avaliacoes
                       FROM vw_avaliacoes_monitoria
                       WHERE id_usuario = %s
                       ORDER BY disciplina""",
                    (id_monitor,),
                )
            else:
                cursor.execute(
                    """SELECT monitor, disciplina, media_nota, total_avaliacoes
                       FROM vw_avaliacoes_monitoria
                       ORDER BY monitor, disciplina"""
                )
            return [
                {
                    "monitor": row[0],
                    "disciplina": row[1],
                    "media_nota": row[2],
                    "total_avaliacoes": row[3],
                }
                for row in cursor.fetchall()
            ]

    def count_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM avaliacoes_tutoria")
            return cursor.fetchone()[0]
