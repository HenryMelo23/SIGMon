from app.models.registro_frequencia import RegistroFrequencia
from app.database.db import get_connection

class FrequenciaRepository:
    def count_nao_validadas(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM registros_frequencia WHERE validado = FALSE")
            return cursor.fetchone()[0]