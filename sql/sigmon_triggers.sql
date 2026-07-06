-- SIGMon - Triggers
-- Executar APOS sigmon_create.sql

-- ============================================================
-- TRIGGER 1: registra auditoria quando o papel do usuario muda.
-- A procedure de aprovacao atualiza usuarios.papel; este trigger
-- prova que a auditoria foi gerada automaticamente pelo banco.
-- ============================================================

CREATE OR REPLACE FUNCTION auditar_mudanca_papel()
RETURNS trigger AS $$
BEGIN
    IF NEW.papel IS DISTINCT FROM OLD.papel THEN
        INSERT INTO auditoria (id_usuario, acao, entidade, detalhes)
        VALUES (
            NEW.id_usuario,
            'MUDANCA_PAPEL',
            'usuarios',
            'Usuario ' || NEW.id_usuario || ' mudou de ' || OLD.papel || ' para ' || NEW.papel
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_auditoria_mudanca_papel
AFTER UPDATE OF papel ON usuarios
FOR EACH ROW EXECUTE FUNCTION auditar_mudanca_papel();

-- ============================================================
-- TRIGGER 2: registra auditoria ao inserir ou alterar dados bancarios.
-- ============================================================

CREATE OR REPLACE FUNCTION auditar_dados_bancarios()
RETURNS trigger AS $$
BEGIN
    INSERT INTO auditoria (id_usuario, acao, entidade, detalhes)
    VALUES (
        NEW.id_usuario,
        TG_OP,
        'dados_bancarios',
        'Dados bancarios do usuario ' || NEW.id_usuario || ' foram ' ||
        CASE TG_OP WHEN 'INSERT' THEN 'inseridos' ELSE 'atualizados' END
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_auditoria_dados_bancarios
AFTER INSERT OR UPDATE ON dados_bancarios
FOR EACH ROW EXECUTE FUNCTION auditar_dados_bancarios();

-- ============================================================
-- TRIGGER 3: ao marcar sessao como realizada, marca o slot como reservado.
-- ============================================================

CREATE OR REPLACE FUNCTION sincronizar_slot_sessao()
RETURNS trigger AS $$
BEGIN
    IF NEW.realizada = TRUE AND OLD.realizada = FALSE THEN
        UPDATE agenda_slots
        SET reservado = TRUE
        WHERE id_slot = NEW.id_slot;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sincronizar_slot
AFTER UPDATE ON sessoes_tutoria
FOR EACH ROW EXECUTE FUNCTION sincronizar_slot_sessao();
