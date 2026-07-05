-- SIGMon - Dados iniciais (seeds)
-- Executar APOS sigmon_create.sql, procedures, views e triggers
-- Cenario: hoje e 2026-07-05
--
-- Fluxo de apresentacao:
--   1. CRUD ao vivo: horarios, disciplinas, turmas (com restricoes FK)
--   2. PDF ao vivo: Pedro loga, cadastra historico de BD com PDF
--   3. Admin aprova o historico de Pedro
--   4. Pedro se candidata ao vivo (edital 2026.1, BD T02)
--   5. Procedure: CALL aprovar_candidatura_e_alocar(2, 2) via psql
--   6. Trigger: auditoria mostra MUDANCA_PAPEL gerado automaticamente
--   7. View: Rafael loga e ve desempenho por disciplina (alimentado por Amanda)

-- ============================================================
-- DEPARTAMENTOS (1)
-- ============================================================

INSERT INTO departamentos (id_departamento, nome, sigla, email) VALUES
(1, 'Departamento de Ciencia da Computacao', 'CIC', 'secretaria@cic.unb.br');

SELECT setval('departamentos_id_departamento_seq', 1);

-- ============================================================
-- USUARIOS (6)
-- 1 admin, 2 professores, 1 monitor (Rafael), 2 estudantes
-- Pedro: sem historico, sem inscricao — faz tudo ao vivo
-- Amanda: ja aprovada em BD, com sessoes e avaliacoes (alimenta a view)
-- ============================================================

INSERT INTO usuarios (id_usuario, id_departamento, nome, email, matricula, papel, senha_hash, ativo, data_cadastro) VALUES
(1, 1, 'Ana Beatriz',     'admin@unb.br',      'ADM001',    'ADMINISTRADOR', '123456', TRUE, '2025-01-10'),
(2, 1, 'Prof. Maristela', 'maristela@unb.br',  'DOC001',    'PROFESSOR',     '123456', TRUE, '2025-01-11'),
(3, 1, 'Prof. Caetano',   'caetano@unb.br',    'DOC002',    'PROFESSOR',     '123456', TRUE, '2025-01-12'),
(4, 1, 'Rafael Mendes',   'monitor@unb.br',    '211000001', 'MONITOR',       '123456', TRUE, '2025-02-01'),
(5, 1, 'Pedro Alves',     'estudante@unb.br',  '231000001', 'ESTUDANTE',     '123456', TRUE, '2025-02-10'),
(6, 1, 'Amanda Silva',    'amanda@unb.br',     '221000042', 'ESTUDANTE',     '123456', TRUE, '2025-02-10');

SELECT setval('usuarios_id_usuario_seq', 6);

-- ============================================================
-- DISCIPLINAS (4)
-- Algoritmos nao esta vinculada a nenhuma turma (para demo de delete sem FK)
-- ============================================================

INSERT INTO disciplinas (id_disciplina, id_departamento, codigo, nome, creditos) VALUES
(1, 1, 'CIC0097', 'Banco de Dados',                           4),
(2, 1, 'CIC0004', 'Algoritmos e Programacao de Computadores', 4),
(3, 1, 'CIC0105', 'Estrutura de Dados',                       4),
(4, 1, 'CIC0116', 'Redes de Computadores',                    4);

SELECT setval('disciplinas_id_disciplina_seq', 4);

-- ============================================================
-- HORARIOS (4)
-- Ter/Qui 14h-15h50: turmas de BD da Maristela (T01 dia, T02 noite)
-- Ter/Qui 10h-11h50: turma de Redes do Caetano
-- Seg/Qua 10h-11h50: turma de ED do Caetano
-- ============================================================

INSERT INTO horarios (id_horario, codigo, descricao, turno, ativo) VALUES
(1, '35T23', 'Ter/Qui 14h-15h50', 'T', TRUE),
(2, '35M12', 'Ter/Qui 10h-11h50', 'M', TRUE),
(3, '24M12', 'Seg/Qua 10h-11h50', 'M', TRUE),
(4, '35N12', 'Ter/Qui 19h-20h50', 'N', TRUE);

SELECT setval('horarios_id_horario_seq', 4);

-- ============================================================
-- TURMAS (4)
-- BD T01: Rafael e monitor aqui
-- BD T02: vaga disponivel para Pedro se candidatar ao vivo
-- ============================================================

INSERT INTO turmas (id_turma, id_disciplina, id_professor, semestre, codigo_turma, id_horario, sala, vagas_monitor, carga_horaria_semanal) VALUES
(1, 1, 2, '2026.1', 'T01', 1, 'PJC BT 036', 1, 12),
(2, 1, 2, '2026.1', 'T02', 4, 'PJC BT 038', 1, 12),
(3, 4, 3, '2026.1', 'T01', 2, 'PJC BT 044', 1, 12),
(4, 3, 3, '2026.1', 'T01', 3, 'LAB CIC 02', 1, 12);

SELECT setval('turmas_id_turma_seq', 4);

-- ============================================================
-- EDITAIS (2)
-- Edital 1 (2025.2): encerrado, gerou Rafael como monitor
-- Edital 2 (2026.1): aberto, Pedro se candidata ao vivo aqui
-- ============================================================

INSERT INTO editais (id_edital, id_departamento, titulo, descricao, semestre, data_inicio, data_fim, nota_minima, data_inicio_monitoria, data_fim_monitoria) VALUES
(1, 1, 'Edital de Monitoria CIC 2025.2', 'Selecao de monitores para o segundo semestre de 2025.', '2025.2', '2025-08-01', '2025-09-15', 'MS', '2025-10-01', '2026-03-15'),
(2, 1, 'Edital de Monitoria CIC 2026.1', 'Selecao de monitores para o primeiro semestre de 2026.', '2026.1', '2026-06-01', '2026-08-01', 'MS', '2026-08-15', '2026-12-20');

SELECT setval('editais_id_edital_seq', 2);

-- ============================================================
-- DOCUMENTOS_ANEXOS (2)
-- 1: historico de Rafael para BD
-- 2: historico de Amanda para BD
-- ============================================================

INSERT INTO documentos_anexos (id_documento, id_usuario, id_edital, id_candidatura, nome_arquivo, tipo_documento, mime_type, conteudo, data_upload) VALUES
(1, 4, NULL, NULL, 'historico_rafael.pdf', 'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2025-09-01'),
(2, 6, NULL, NULL, 'historico_amanda.pdf', 'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2025-09-01');

SELECT setval('documentos_anexos_id_documento_seq', 2);

-- ============================================================
-- HISTORICO_ESCOLAR (2)
-- Rafael: BD SS 2025.1 APROVADO (qualifica para ser monitor de BD)
-- Amanda: BD MS 2025.1 APROVADO (qualifica para se inscrever na turma)
-- Pedro: sem historico — vai cadastrar ao vivo durante a apresentacao
-- ============================================================

INSERT INTO historico_escolar (id_historico, id_estudante, id_disciplina, id_documento, mencao, semestre, status, justificativa, data_cadastro) VALUES
(1, 4, 1, 1, 'SS', '2025.1', 'APROVADO', NULL, '2025-09-01'),
(2, 6, 1, 2, 'MS', '2025.1', 'APROVADO', NULL, '2025-09-01');

SELECT setval('historico_escolar_id_historico_seq', 2);

-- ============================================================
-- INSCRICOES_TURMAS (1)
-- Amanda inscrita em BD T01 (APROVADA) para ver e reservar agenda de Rafael
-- Pedro: sem inscricao — candidatara ao edital, nao precisa de inscricao na turma
-- ============================================================

INSERT INTO inscricoes_turmas (id_inscricao, id_estudante, id_turma, id_documento, status, justificativa, data_cadastro) VALUES
(1, 6, 1, NULL, 'APROVADA', NULL, '2026-02-15');

SELECT setval('inscricoes_turmas_id_inscricao_seq', 1);

-- ============================================================
-- CANDIDATURAS (1)
-- Rafael candidatou-se no edital 2025.2 para BD T01 e foi aprovado
-- A candidatura de Pedro (id=2) sera criada ao vivo durante a apresentacao
-- ============================================================

INSERT INTO candidaturas (id_candidatura, id_edital, id_estudante, id_turma, data_inscricao, ira, nota_disciplina, status) VALUES
(1, 1, 4, 1, '2025-09-05', 4.50, 'SS', 'APROVADA');

SELECT setval('candidaturas_id_candidatura_seq', 1);

-- ============================================================
-- ALOCACOES_MONITORES (1)
-- Rafael alocado em BD T01 com Maristela (gerado pelo edital 2025.2)
-- ============================================================

INSERT INTO alocacoes_monitores (id_alocacao, id_candidatura, id_monitor, id_disciplina, id_turma, id_professor, data_inicio, data_fim, carga_horaria_semanal, status) VALUES
(1, 1, 4, 1, 1, 2, '2025-10-01', '2026-03-15', 12, 'ATIVA');

SELECT setval('alocacoes_monitores_id_alocacao_seq', 1);

-- ============================================================
-- AGENDA_SLOTS (4)
-- Slots 1 e 2: reservados (tem sessoes com Amanda)
-- Slots 3 e 4: disponiveis (para demo de reserva ou consulta na apresentacao)
-- ============================================================

INSERT INTO agenda_slots (id_slot, id_alocacao, data_slot, hora_inicio, hora_fim, local_atendimento, modalidade, reservado) VALUES
(1, 1, '2026-07-08', '14:00', '15:00', 'PJC BT 036',                 'PRESENCIAL', TRUE),
(2, 1, '2026-07-10', '14:00', '15:00', 'meet.google.com/abc-def-ghi', 'ONLINE',     TRUE),
(3, 1, '2026-07-15', '14:00', '15:00', 'PJC BT 036',                 'PRESENCIAL', FALSE),
(4, 1, '2026-07-17', '14:00', '15:00', 'meet.google.com/xyz-uvw-klm', 'ONLINE',     FALSE);

SELECT setval('agenda_slots_id_slot_seq', 4);

-- ============================================================
-- SESSOES_TUTORIA (2)
-- Amanda reservou slots 1 e 2, ambas realizadas
-- ============================================================

INSERT INTO sessoes_tutoria (id_sessao, id_slot, id_estudante, assunto, realizada, data_registro) VALUES
(1, 1, 6, 'Modelagem ER e Normalizacao', TRUE, '2026-07-08'),
(2, 2, 6, 'SQL Joins e Subconsultas',    TRUE, '2026-07-10');

SELECT setval('sessoes_tutoria_id_sessao_seq', 2);

-- ============================================================
-- AVALIACOES_TUTORIA (2)
-- Amanda avaliou as duas sessoes (alimenta a vw_avaliacoes_monitoria)
-- ============================================================

INSERT INTO avaliacoes_tutoria (id_avaliacao, id_sessao, id_estudante, nota, comentario, data_avaliacao) VALUES
(1, 1, 6, 5, 'Explicacao muito clara sobre normalizacao e ER.', '2026-07-08'),
(2, 2, 6, 4, 'Bom atendimento, exemplos praticos muito uteis.', '2026-07-10');

SELECT setval('avaliacoes_tutoria_id_avaliacao_seq', 2);
