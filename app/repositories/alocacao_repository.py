from app.database.db import get_connection
from app.models.alocacao import AlocacaoMonitor

_JOIN = """
    SELECT a.*, um.nome AS monitor_nome, d.nome AS disciplina_nome,
           t.codigo_turma, up.nome AS professor_nome
    FROM alocacoes_monitores a
    JOIN usuarios um ON a.id_monitor = um.id_usuario
    JOIN disciplinas d ON a.id_disciplina = d.id_disciplina
    JOIN turmas t ON a.id_turma = t.id_turma
    JOIN usuarios up ON a.id_professor = up.id_usuario
"""


class AlocacaoRepository:
    def get_by_id(self, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(_JOIN + "WHERE a.id_alocacao = %s", (id,))
            row = cursor.fetchone()
            return AlocacaoMonitor(*row) if row else None

    def count_ativos(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM alocacoes_monitores WHERE status = 'ATIVA'")
            return cursor.fetchone()[0]

    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(_JOIN + "ORDER BY a.data_inicio DESC")
            return [AlocacaoMonitor(*row) for row in cursor.fetchall()]

    def list_by_monitor(self, id_monitor):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(_JOIN + "WHERE a.id_monitor = %s ORDER BY a.data_inicio DESC", (id_monitor,))
            return [AlocacaoMonitor(*row) for row in cursor.fetchall()]

    def list_by_professor(self, id_professor):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(_JOIN + "WHERE a.id_professor = %s ORDER BY a.data_inicio DESC", (id_professor,))
            return [AlocacaoMonitor(*row) for row in cursor.fetchall()]

    def find_by_candidatura(self, id_candidatura):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_alocacao FROM alocacoes_monitores WHERE id_candidatura = %s",
                (id_candidatura,)
            )
            return cursor.fetchone() is not None

    def create(self, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO alocacoes_monitores
                    (id_candidatura, id_monitor, id_disciplina, id_turma, id_professor,
                     data_inicio, data_fim, carga_horaria_semanal, status)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                RETURNING id_alocacao
                """,
                (
                    payload["id_candidatura"],
                    payload["id_monitor"],
                    payload["id_disciplina"],
                    payload["id_turma"],
                    payload["id_professor"],
                    payload["data_inicio"],
                    payload["data_fim"],
                    payload["carga_horaria_semanal"],
                    payload["status"],
                )
            )
            conn.commit()
            id_alocacao = cursor.fetchone()[0]
            return self.get_by_id(id_alocacao)

    def update(self, id_alocacao, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE alocacoes_monitores SET status = %s WHERE id_alocacao = %s",
                (payload["status"], id_alocacao)
            )
            conn.commit()

    def reativar_por_candidatura(self, id_candidatura):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE alocacoes_monitores SET status = 'ATIVA' WHERE id_candidatura = %s",
                (id_candidatura,)
            )
            conn.commit()

    def encerrar_por_candidatura(self, id_candidatura):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE alocacoes_monitores SET status = 'ENCERRADA' WHERE id_candidatura = %s",
                (id_candidatura,)
            )
            conn.commit()

    def encerrar_todas_ativas(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE alocacoes_monitores SET status = 'ENCERRADA' WHERE status = 'ATIVA'"
            )
            conn.commit()
            return cursor.rowcount
