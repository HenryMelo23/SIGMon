-- SIGMon - Dados iniciais (seeds)
-- Executar APOS sigmon_create.sql
-- Cenario: hoje e 2026-07-02
--   Edital 2 (2026.1 Complementar) encerrou em 2026-04-30 e gerou Mateus e Beatriz como monitores
--   Edital 1 (2026.1 Principal) esta aberto (2026-06-01 a 2026-07-20) com candidaturas ativas

-- ============================================================
-- DEPARTAMENTOS (5 registros)
-- ============================================================

INSERT INTO departamentos (id_departamento, nome, sigla, email) VALUES
(1, 'Departamento de Ciencia da Computacao', 'CIC', 'secretaria@cic.unb.br'),
(2, 'Departamento de Matematica',            'MAT', 'mat@unb.br'),
(3, 'Departamento de Fisica',                'FIS', 'fis@unb.br'),
(4, 'Departamento de Estatistica',           'EST', 'est@unb.br'),
(5, 'Departamento de Engenharia Eletrica',   'ENE', 'ene@unb.br');

SELECT setval('departamentos_id_departamento_seq', 5);

-- ============================================================
-- USUARIOS (8 registros)
-- Mateus (6) e Beatriz (7) sao MONITOR pois foram aprovados no edital 2
-- ============================================================

INSERT INTO usuarios (id_usuario, id_departamento, nome, email, matricula, papel, senha_hash, ativo, data_cadastro) VALUES
(1, 1, 'Ana Beatriz Martins',   'admin@unb.br',       'ADM001',    'ADMINISTRADOR', '123456', TRUE, '2026-01-10'),
(2, 1, 'Prof. Rafael Nogueira', 'professor@unb.br',   'DOC742',    'PROFESSOR',     '123456', TRUE, '2026-01-11'),
(3, 1, 'Prof. Mariana Costa',   'mariana@unb.br',     'DOC801',    'PROFESSOR',     '123456', TRUE, '2026-01-15'),
(4, 1, 'Luisa Carvalho',        'estudante@unb.br',   '231045678', 'ESTUDANTE',     '123456', TRUE, '2026-02-02'),
(5, 1, 'Camila Rocha',          'camila@unb.br',      '230091234', 'ESTUDANTE',     '123456', TRUE, '2026-01-20'),
(6, 1, 'Mateus Henrique Lima',  'monitor@unb.br',     '211098765', 'MONITOR',       '123456', TRUE, '2026-02-08'),
(7, 1, 'Beatriz Oliveira',      'beatriz@unb.br',     '220034512', 'MONITOR',       '123456', TRUE, '2026-02-10'),
(8, 1, 'Pedro Alves',           'pedro@unb.br',       '230078934', 'ESTUDANTE',     '123456', TRUE, '2026-02-12');

SELECT setval('usuarios_id_usuario_seq', 8);

-- ============================================================
-- DISCIPLINAS (5 registros)
-- ============================================================

INSERT INTO disciplinas (id_disciplina, id_departamento, codigo, nome, creditos) VALUES
(1, 1, 'CIC0097', 'Banco de Dados',                   4),
(2, 1, 'CIC0105', 'Estruturas de Dados',              4),
(3, 1, 'CIC0004', 'Algoritmos e Programacao',         4),
(4, 1, 'CIC0210', 'Programacao Orientada a Objetos',  4),
(5, 2, 'MAT0025', 'Calculo 1',                        4);

SELECT setval('disciplinas_id_disciplina_seq', 5);

-- ============================================================
-- HORARIOS (5 registros)
-- ============================================================

INSERT INTO horarios (id_horario, codigo, descricao, turno, ativo) VALUES
(1, '246M34', 'Seg/Qua/Sex 10h-11h50', 'M', TRUE),
(2, '35T23',  'Ter/Qui 14h-15h50',     'T', TRUE),
(3, '6M1234', 'Sex 08h-11h50',         'M', TRUE),
(4, '46T45',  'Qua/Sex 16h-17h50',     'T', TRUE),
(5, '35M12',  'Ter/Qui 08h-09h50',     'M', TRUE);

SELECT setval('horarios_id_horario_seq', 5);

-- ============================================================
-- TURMAS (5 registros) - todas em 2026.1
-- turma 1 (BD)  : 1 vaga, ocupada por Mateus (via edital 2)
-- turma 2 (ED)  : 1 vaga, ocupada por Beatriz (via edital 2)
-- turmas 3,4,5  : vagas disponiveis para edital 1 (aberto)
-- ============================================================

INSERT INTO turmas (id_turma, id_disciplina, id_professor, semestre, codigo_turma, id_horario, sala, vagas_monitor, carga_horaria_semanal) VALUES
(1, 1, 2, '2026.1', 'T01', 1, 'PJC BT 036', 1, 12),
(2, 2, 2, '2026.1', 'T01', 2, 'LAB CIC 02', 1, 12),
(3, 3, 3, '2026.1', 'T01', 3, 'PJC BT 044', 2,  8),
(4, 4, 2, '2026.1', 'T01', 4, 'LAB CIC 01', 1, 10),
(5, 3, 3, '2026.1', 'T02', 5, 'PJC BT 048', 1,  8);

SELECT setval('turmas_id_turma_seq', 5);

-- ============================================================
-- EDITAIS (5 registros)
-- Edital 1: ABERTO hoje (2026-06-01 a 2026-07-20)
-- Edital 2: ENCERRADO (2026-04-01 a 2026-04-30) - gerou Mateus e Beatriz
-- Edital 3: ABERTO hoje para 2026.2 (2026-07-01 a 2026-08-10)
-- Edital 4: ENCERRADO (2026-05-01 a 2026-06-15)
-- Edital 5: ABERTO hoje (2026-06-10 a 2026-07-10)
-- ============================================================

INSERT INTO editais (id_edital, id_departamento, titulo, descricao, semestre, data_inicio, data_fim, nota_minima, data_inicio_monitoria, data_fim_monitoria) VALUES
(1, 1, 'Edital de Monitoria CIC 2026.1',       'Selecao principal para monitoria 2026.1.',         '2026.1', '2026-06-01', '2026-07-20', 'MS', '2026-08-01', '2026-12-15'),
(2, 1, 'Edital Complementar CIC 2026.1',       'Chamada complementar encerrada em abril.',         '2026.1', '2026-04-01', '2026-04-30', 'MS', '2026-05-01', '2026-11-30'),
(3, 1, 'Edital de Monitoria CIC 2026.2',       'Selecao para o segundo semestre de 2026.',         '2026.2', '2026-07-01', '2026-08-10', 'MS', '2026-08-15', '2026-12-20'),
(4, 1, 'Edital Extra CIC 2026.1',              'Chamada extra encerrada em junho.',                '2026.1', '2026-05-01', '2026-06-15', 'MS', '2026-07-01', '2026-11-30'),
(5, 1, 'Edital Algoritmos CIC 2026.1',         'Apoio especifico para disciplinas de algoritmos.', '2026.1', '2026-06-10', '2026-07-10', 'SS', '2026-08-01', '2026-12-15');

SELECT setval('editais_id_edital_seq', 5);

-- ============================================================
-- DOCUMENTOS_ANEXOS (5 registros)
-- PDFs de historico escolar enviados pelos estudantes
-- id_edital e id_candidatura sao NULL pois sao documentos de historico
-- ============================================================

INSERT INTO documentos_anexos (id_documento, id_usuario, id_edital, id_candidatura, nome_arquivo, tipo_documento, mime_type, conteudo, data_upload) VALUES
(1, 6, NULL, NULL, 'historico_mateus.pdf',  'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-01-10'),
(2, 7, NULL, NULL, 'historico_beatriz.pdf', 'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-01-12'),
(3, 8, NULL, NULL, 'historico_pedro.pdf',   'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-01-15'),
(4, 4, NULL, NULL, 'historico_luisa.pdf',   'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-01-10'),
(5, 4, NULL, NULL, 'historico_luisa_2.pdf', 'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-06-01');

SELECT setval('documentos_anexos_id_documento_seq', 5);

-- ============================================================
-- HISTORICO_ESCOLAR (8 registros)
-- Mateus (6): BD SS, ED MS  -> elegivel para turmas CIC com mencao >= MS
-- Beatriz (7): ED SS        -> elegivel para turmas de ED
-- Pedro (8): Algo MS, POO MS -> elegivel para turmas 3,4,5
-- Luisa (4): BD SS, Algo SS  -> elegivel para turmas 1,3,5 (BD sem vaga no ed2, disponivel no ed1)
-- ============================================================

INSERT INTO historico_escolar (id_historico, id_estudante, id_disciplina, id_documento, mencao, semestre, status, justificativa, data_cadastro) VALUES
(1, 6, 1, 1, 'SS', '2025.1', 'APROVADO', NULL, '2026-01-10'),
(2, 6, 2, 1, 'MS', '2025.1', 'APROVADO', NULL, '2026-01-10'),
(3, 7, 2, 2, 'SS', '2025.1', 'APROVADO', NULL, '2026-01-12'),
(4, 8, 3, 3, 'MS', '2025.1', 'APROVADO', NULL, '2026-01-15'),
(5, 8, 4, 3, 'MS', '2025.1', 'APROVADO', NULL, '2026-01-15'),
(6, 4, 1, 4, 'SS', '2025.1', 'APROVADO', NULL, '2026-01-10'),
(7, 4, 3, 4, 'SS', '2025.1', 'APROVADO', NULL, '2026-01-10'),
(8, 4, 2, 5, 'MM', '2025.2', 'PENDENTE', NULL, '2026-06-01');

SELECT setval('historico_escolar_id_historico_seq', 8);

-- ============================================================
-- INSCRICOES_TURMAS (3 registros)
-- Luisa (4) em BD T01 -> ve slots do Mateus
-- Pedro (8) em ED T01 -> ve slots da Beatriz
-- Mateus (6) em ED T01 como estudante -> ve slots da Beatriz tambem
-- ============================================================

INSERT INTO inscricoes_turmas (id_inscricao, id_estudante, id_turma, id_documento, status, justificativa, data_cadastro) VALUES
(1, 4, 1, NULL, 'APROVADA', NULL, '2026-02-10'),
(2, 8, 2, NULL, 'APROVADA', NULL, '2026-02-12'),
(3, 6, 2, NULL, 'APROVADA', NULL, '2026-02-08');

SELECT setval('inscricoes_turmas_id_inscricao_seq', 3);

-- ============================================================
-- CANDIDATURAS (8 registros)
-- 1,2: APROVADA no edital 2 (encerrado) -> geraram Mateus e Beatriz como monitores
-- 3,4: EM_ANALISE/INSCRITA no edital 1 (aberto) - Pedro e Luisa
-- 5,6: INSCRITA no edital 1 - Pedro (POO) e Luisa (Algo T02)
-- 7: REPROVADA no edital 4 (encerrado) - Pedro
-- 8: CANCELADA no edital 4 - Beatriz (cancelou antes de se candidatar no edital 2)
-- ============================================================

INSERT INTO candidaturas (id_candidatura, id_edital, id_estudante, id_turma, data_inscricao, ira, nota_disciplina, status) VALUES
(1, 2, 6, 1, '2026-04-05', 4.35, 'SS', 'APROVADA'),
(2, 2, 7, 2, '2026-04-06', 4.62, 'SS', 'APROVADA'),
(3, 1, 8, 3, '2026-06-10', 4.10, 'MS', 'EM_ANALISE'),
(4, 1, 4, 3, '2026-06-11', 4.50, 'SS', 'INSCRITA'),
(5, 1, 8, 4, '2026-06-10', 4.10, 'MS', 'INSCRITA'),
(6, 1, 4, 5, '2026-06-11', 4.50, 'SS', 'INSCRITA'),
(7, 4, 8, 3, '2026-05-12', 4.10, 'MS', 'REPROVADA'),
(8, 4, 7, 2, '2026-05-08', 4.20, 'SS', 'CANCELADA');

SELECT setval('candidaturas_id_candidatura_seq', 8);

-- ============================================================
-- ALOCACOES_MONITORES (2 registros)
-- Geradas automaticamente pela aprovacao das candidaturas 1 e 2
-- Datas vem do edital 2: monitoria 2026-05-01 a 2026-11-30
-- Carga horaria vem das turmas: turma 1 = 12h, turma 2 = 12h
-- ============================================================

INSERT INTO alocacoes_monitores (id_alocacao, id_candidatura, id_monitor, id_disciplina, id_turma, id_professor, data_inicio, data_fim, carga_horaria_semanal, status) VALUES
(1, 1, 6, 1, 1, 2, '2026-05-01', '2026-11-30', 12, 'ATIVA'),
(2, 2, 7, 2, 2, 2, '2026-05-01', '2026-11-30', 12, 'ATIVA');

SELECT setval('alocacoes_monitores_id_alocacao_seq', 2);

-- ============================================================
-- AGENDA_SLOTS (5 registros)
-- Slots de atendimento das alocacoes ativas
-- ============================================================

INSERT INTO agenda_slots (id_slot, id_alocacao, data_slot, hora_inicio, hora_fim, local_atendimento, modalidade, reservado) VALUES
(1, 1, '2026-07-07', '14:00', '15:00', 'Laboratorio CIC 02', 'PRESENCIAL', TRUE),
(2, 1, '2026-07-09', '14:00', '15:00', 'Google Meet',        'ONLINE',     TRUE),
(3, 2, '2026-07-08', '16:00', '17:00', 'Laboratorio CIC 01', 'PRESENCIAL', TRUE),
(4, 2, '2026-07-10', '16:00', '17:00', 'Microsoft Teams',    'ONLINE',     TRUE),
(5, 1, '2026-07-14', '14:00', '15:00', 'Laboratorio CIC 02', 'PRESENCIAL', TRUE);

SELECT setval('agenda_slots_id_slot_seq', 5);

-- ============================================================
-- SESSOES_TUTORIA (5 registros)
-- Slots 1-5 reservados com sessao.
-- ============================================================

INSERT INTO sessoes_tutoria (id_sessao, id_slot, id_estudante, assunto, realizada, data_registro) VALUES
(1, 1, 4, 'Modelagem ER',      TRUE,  '2026-07-07'),
(2, 2, 4, 'SQL Joins',         TRUE,  '2026-07-09'),
(3, 3, 8, 'Arvores Binarias',  TRUE,  '2026-07-08'),
(4, 4, 8, 'Listas Ligadas',    TRUE,  '2026-07-10'),
(5, 5, 8, 'Recursao',          FALSE, '2026-07-14');

SELECT setval('sessoes_tutoria_id_sessao_seq', 5);

-- ============================================================
-- AVALIACOES_TUTORIA (5 registros)
-- ============================================================

INSERT INTO avaliacoes_tutoria (id_avaliacao, id_sessao, id_estudante, nota, comentario, data_avaliacao) VALUES
(1, 1, 4, 5, 'Atendimento muito claro e objetivo.',            '2026-07-07'),
(2, 2, 4, 5, 'Excelente explicacao sobre SQL Joins.',          '2026-07-09'),
(3, 3, 8, 4, 'Boa explicacao, poderia ter mais exemplos.',     '2026-07-08'),
(4, 4, 8, 4, 'Bom atendimento, conteudo bem explicado.',       '2026-07-10');

SELECT setval('avaliacoes_tutoria_id_avaliacao_seq', 4);
