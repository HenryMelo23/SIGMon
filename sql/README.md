# SQL planejado para o SIGMon

Esta pasta documenta a evolução prevista para PostgreSQL. A aplicação atual usa repositories em memória, mas a fronteira de persistência foi mantida nos módulos `app/repositories/`.

Quando o banco real for conectado, a equipe pode substituir os repositories mockados por implementações SQLAlchemy ou psycopg2, mantendo services e routes praticamente iguais.
