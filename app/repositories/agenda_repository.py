from app.database.db import get_connection
from app.models.agenda_slot import AgendaSlot

_JOIN = """
    SELECT s.*, u.nome AS monitor_nome, d.nome AS disciplina_nome, t.codigo_turma
    FROM agenda_slots s
    JOIN alocacoes_monitores a ON s.id_alocacao = a.id_alocacao
    JOIN usuarios u ON a.id_monitor = u.id_usuario
    JOIN disciplinas d ON a.id_disciplina = d.id_disciplina
    JOIN turmas t ON a.id_turma = t.id_turma
"""


class AgendaRepository:
    def get_by_id(self, id_slot):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(_JOIN + "WHERE s.id_slot = %s", (id_slot,))
            row = cursor.fetchone()
            return AgendaSlot(*row) if row else None

    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(_JOIN + "ORDER BY s.data_slot, s.hora_inicio")
            return [AgendaSlot(*row) for row in cursor.fetchall()]

    def list_by_monitor(self, id_monitor):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                _JOIN + "WHERE a.id_monitor = %s ORDER BY s.data_slot, s.hora_inicio",
                (id_monitor,)
            )
            return [AgendaSlot(*row) for row in cursor.fetchall()]

    def list_by_turmas_inscritas(self, id_estudante):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                _JOIN + """
                WHERE a.id_turma IN (
                    SELECT id_turma FROM inscricoes_turmas
                    WHERE id_estudante = %s AND status = 'APROVADA'
                )
                ORDER BY s.data_slot, s.hora_inicio
                """,
                (id_estudante,)
            )
            return [AgendaSlot(*row) for row in cursor.fetchall()]

    def list_para_monitor(self, id_monitor):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                _JOIN + """
                WHERE a.id_monitor = %s
                   OR a.id_turma IN (
                       SELECT id_turma FROM inscricoes_turmas
                       WHERE id_estudante = %s AND status = 'APROVADA'
                   )
                ORDER BY s.data_slot, s.hora_inicio
                """,
                (id_monitor, id_monitor)
            )
            return [AgendaSlot(*row) for row in cursor.fetchall()]

    def list_disponiveis(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                _JOIN + "WHERE s.reservado = FALSE ORDER BY s.data_slot, s.hora_inicio"
            )
            return [AgendaSlot(*row) for row in cursor.fetchall()]

    def create(self, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO agenda_slots (id_alocacao, data_slot, hora_inicio, hora_fim,
                    local_atendimento, modalidade, reservado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_slot
                """,
                (
                    payload["id_alocacao"],
                    payload["data_slot"],
                    payload["hora_inicio"],
                    payload["hora_fim"],
                    payload["local_atendimento"],
                    payload["modalidade"],
                    payload.get("reservado", False),
                )
            )
            conn.commit()
            id_slot = cursor.fetchone()[0]
            return self.get_by_id(id_slot)

    def marcar_reservado(self, id_slot, reservado=True):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE agenda_slots SET reservado = %s WHERE id_slot = %s",
                (reservado, id_slot)
            )
            conn.commit()
