from app.database.db import get_connection
from app.models.agenda_slot import AgendaSlot

class AgendaRepository:
    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM agenda_slots")
            rows = cursor.fetchall()
            return [AgendaSlot(*row) for row in rows]