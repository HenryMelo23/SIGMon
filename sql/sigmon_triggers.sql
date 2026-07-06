-- SIGMon - Triggers
-- Executar APOS sigmon_create.sql

-- ============================================================
-- TRIGGER: registra na auditoria toda mudança de papel de usuário
--
-- Quando o papel de um usuário muda (ex: ESTUDANTE → MONITOR),
-- o banco registra automaticamente quem mudou, de qual papel
-- para qual papel, e quando — independente de ter sido feito
-- pelo sistema ou diretamente no banco.
--
-- Ativado por: UPDATE em usuarios quando NEW.papel != OLD.papel
-- ============================================================

CREATE OR REPLACE FUNCTION auditar_mudanca_papel()
RETURNS trigger AS $$
BEGIN
    IF NEW.papel <> OLD.papel THEN
        INSERT INTO auditoria (id_usuario, acao, entidade, detalhes)
        VALUES (
            NEW.id_usuario,
            'MUDANCA_PAPEL',
            'usuarios',
            'Papel alterado de ' || OLD.papel || ' para ' || NEW.papel
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_auditoria_mudanca_papel
AFTER UPDATE ON usuarios
FOR EACH ROW EXECUTE FUNCTION auditar_mudanca_papel();
