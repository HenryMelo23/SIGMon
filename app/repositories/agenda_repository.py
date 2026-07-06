from app.database.db import get_connection
from app.models.agenda_slot import AgendaSlot

class AgendaRepository:
    def _from_row(self, row):
        return AgendaSlot(*row) if row else None

    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM agenda_slots ORDER BY data_slot, hora_inicio")
            rows = cursor.fetchall()
            return [AgendaSlot(*row) for row in rows]

    def list_disponiveis(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM agenda_slots
                   WHERE reservado = FALSE OR modalidade = 'ONLINE'
                   ORDER BY data_slot, hora_inicio"""
            )
            return [AgendaSlot(*row) for row in cursor.fetchall()]

    def get_by_id(self, id_slot):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM agenda_slots WHERE id_slot = %s", (id_slot,))
            return self._from_row(cursor.fetchone())

    def create(self, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO agenda_slots
                   (id_alocacao, data_slot, hora_inicio, hora_fim, local_atendimento, modalidade, reservado)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   RETURNING *""",
                (
                    payload["id_alocacao"],
                    payload["data_slot"],
                    payload["hora_inicio"],
                    payload["hora_fim"],
                    payload["local_atendimento"],
                    payload["modalidade"],
                    payload["reservado"],
                ),
            )
            conn.commit()
            return self._from_row(cursor.fetchone())

    def update(self, id_slot, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE agenda_slots SET reservado = %s WHERE id_slot = %s RETURNING *",
                (payload["reservado"], id_slot),
            )
            conn.commit()
            return self._from_row(cursor.fetchone())
