-- Views planejadas.

CREATE OR REPLACE VIEW vw_monitores_ativos AS
SELECT u.id_usuario, u.nome, u.email
FROM usuarios u
JOIN alocacoes_monitores a ON a.id_monitor = u.id_usuario
WHERE u.ativo = TRUE AND a.status = 'ATIVA';

-- Planejado:
-- vw_dashboard_professor: turmas, candidaturas e frequências pendentes.
-- vw_dashboard_administrador: editais, vagas, candidaturas e alocações.
-- vw_financeiro_frequencias_validadas: dados para pagamento.
-- vw_avaliacoes_monitoria: médias por monitor/disciplina.
