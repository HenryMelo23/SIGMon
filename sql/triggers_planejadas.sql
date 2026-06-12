-- Triggers planejadas para PostgreSQL.

-- Exemplo: validar nota mínima institucional.
CREATE OR REPLACE FUNCTION validar_nota_minima_edital()
RETURNS trigger AS $$
BEGIN
  IF NEW.nota_minima < 7.0 THEN
    RAISE EXCEPTION 'A nota mínima do edital deve ser maior ou igual a 7.0';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- CREATE TRIGGER trg_validar_nota_minima
-- BEFORE INSERT OR UPDATE ON editais
-- FOR EACH ROW EXECUTE FUNCTION validar_nota_minima_edital();

-- Planejado:
-- - auditar acesso a dados_bancarios;
-- - auditar alteração de status de candidatura;
-- - manter histórico de validação de frequência.
