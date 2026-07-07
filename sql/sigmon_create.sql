-- SIGMon - Sistema Integrado de Gestao de Monitoria
-- Script SQL completo de criacao do banco de dados
-- SGBD: PostgreSQL
-- Integrantes: Luis Henrique Bessa de Melo e Carlos Victor Albuquerque Oliveira

CREATE EXTENSION IF NOT EXISTS unaccent;

-- Para executar:
--   sudo -u postgres psql
--   CREATE DATABASE sigmon;
--   \c sigmon
--   \i /caminho/para/sigmon_create.sql

-- ============================================================
-- REMOCAO SEGURA (ordem inversa de dependencia)
-- ============================================================

DROP TABLE IF EXISTS avaliacoes_tutoria     CASCADE;
DROP TABLE IF EXISTS sessoes_tutoria        CASCADE;
DROP TABLE IF EXISTS agenda_slots           CASCADE;
DROP TABLE IF EXISTS inscricoes_turmas      CASCADE;
DROP TABLE IF EXISTS historico_escolar      CASCADE;
DROP TABLE IF EXISTS documentos_anexos      CASCADE;
DROP TABLE IF EXISTS alocacoes_monitores    CASCADE;
DROP TABLE IF EXISTS candidaturas           CASCADE;
DROP TABLE IF EXISTS editais                CASCADE;
DROP TABLE IF EXISTS turmas                 CASCADE;
DROP TABLE IF EXISTS horarios               CASCADE;
DROP TABLE IF EXISTS disciplinas            CASCADE;
DROP TABLE IF EXISTS usuarios               CASCADE;
DROP TABLE IF EXISTS departamentos          CASCADE;
DROP TABLE IF EXISTS auditoria              CASCADE;

-- ============================================================
-- TABELAS
-- ============================================================

CREATE TABLE departamentos (
    id_departamento SERIAL PRIMARY KEY,
    nome            VARCHAR(120) NOT NULL,
    sigla           VARCHAR(20)  NOT NULL UNIQUE,
    email           VARCHAR(120)
);

CREATE TABLE usuarios (
    id_usuario      SERIAL PRIMARY KEY,
    id_departamento INTEGER      REFERENCES departamentos(id_departamento),
    nome            VARCHAR(150) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    matricula       VARCHAR(30)  UNIQUE,
    papel           VARCHAR(20)  NOT NULL CHECK (
                        papel IN ('ESTUDANTE', 'MONITOR', 'PROFESSOR', 'ADMINISTRADOR')
                    ),
    senha_hash      VARCHAR(255),
    ativo           BOOLEAN      NOT NULL DEFAULT TRUE,
    data_cadastro   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE disciplinas (
    id_disciplina   SERIAL PRIMARY KEY,
    id_departamento INTEGER      NOT NULL REFERENCES departamentos(id_departamento),
    codigo          VARCHAR(20)  NOT NULL UNIQUE,
    nome            VARCHAR(150) NOT NULL,
    creditos        INTEGER      NOT NULL CHECK (creditos > 0)
);

CREATE TABLE horarios (
    id_horario  SERIAL PRIMARY KEY,
    codigo      VARCHAR(20)  NOT NULL UNIQUE,
    descricao   VARCHAR(80)  NOT NULL,
    turno       CHAR(1)      NOT NULL CHECK (turno IN ('M', 'T', 'N')),
    ativo       BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE TABLE turmas (
    id_turma        SERIAL PRIMARY KEY,
    id_disciplina   INTEGER      NOT NULL REFERENCES disciplinas(id_disciplina),
    id_professor    INTEGER      NOT NULL REFERENCES usuarios(id_usuario),
    semestre        VARCHAR(10)  NOT NULL,
    codigo_turma    VARCHAR(20)  NOT NULL,
id_horario      INTEGER      REFERENCES horarios(id_horario),
    sala            VARCHAR(80),
    vagas_monitor         INTEGER NOT NULL DEFAULT 0 CHECK (vagas_monitor >= 0),
    carga_horaria_semanal INTEGER NOT NULL DEFAULT 12 CHECK (carga_horaria_semanal > 0),
    UNIQUE (id_disciplina, semestre, codigo_turma)
);

CREATE TABLE editais (
    id_edital         SERIAL PRIMARY KEY,
    id_departamento   INTEGER       NOT NULL REFERENCES departamentos(id_departamento),
    titulo            VARCHAR(180)  NOT NULL,
    descricao         TEXT,
    semestre          VARCHAR(10)   NOT NULL,
    data_inicio       DATE          NOT NULL,
    data_fim          DATE          NOT NULL,
    nota_minima             VARCHAR(2) NOT NULL DEFAULT 'MS' CHECK (nota_minima IN ('SS', 'MS', 'MM', 'MI', 'II', 'SR')),
    data_inicio_monitoria   DATE       NOT NULL,
    data_fim_monitoria      DATE       NOT NULL,
    CHECK (data_fim >= data_inicio),
    CHECK (data_fim_monitoria >= data_inicio_monitoria)
);

CREATE TABLE candidaturas (
    id_candidatura  SERIAL PRIMARY KEY,
    id_edital       INTEGER      NOT NULL REFERENCES editais(id_edital),
    id_estudante    INTEGER      NOT NULL REFERENCES usuarios(id_usuario),
    id_turma        INTEGER      NOT NULL REFERENCES turmas(id_turma),
    data_inscricao  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ira             NUMERIC(4,2) CHECK (ira BETWEEN 0 AND 5),
    nota_disciplina VARCHAR(2)   CHECK (nota_disciplina IN ('SS', 'MS', 'MM', 'MI', 'II', 'SR')),
    status          VARCHAR(20)  NOT NULL DEFAULT 'INSCRITA' CHECK (
                        status IN ('INSCRITA', 'EM_ANALISE', 'APROVADA', 'REPROVADA', 'CANCELADA')
                    ),
    UNIQUE (id_edital, id_estudante, id_turma)
);

CREATE TABLE alocacoes_monitores (
    id_alocacao           SERIAL PRIMARY KEY,
    id_candidatura        INTEGER NOT NULL UNIQUE REFERENCES candidaturas(id_candidatura),
    id_monitor            INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    id_disciplina         INTEGER NOT NULL REFERENCES disciplinas(id_disciplina),
    id_turma              INTEGER REFERENCES turmas(id_turma),
    id_professor          INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    data_inicio           DATE    NOT NULL,
    data_fim              DATE    NOT NULL,
    carga_horaria_semanal INTEGER NOT NULL CHECK (carga_horaria_semanal > 0),
    status                VARCHAR(20) NOT NULL DEFAULT 'ATIVA' CHECK (
                              status IN ('ATIVA', 'ENCERRADA', 'SUSPENSA')
                          ),
    CHECK (data_fim >= data_inicio)
);

-- Armazena documentos binarios (PDF, imagens) vinculados a usuarios, editais ou candidaturas.
-- O campo conteudo usa BYTEA para armazenar o arquivo diretamente no banco.
CREATE TABLE documentos_anexos (
    id_documento    SERIAL PRIMARY KEY,
    id_usuario      INTEGER       REFERENCES usuarios(id_usuario),
    nome_arquivo    VARCHAR(180)  NOT NULL,
    tipo_documento  VARCHAR(60)   NOT NULL,
    mime_type       VARCHAR(100)  NOT NULL,
    conteudo        BYTEA,
    data_upload     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE historico_escolar (
    id_historico    SERIAL PRIMARY KEY,
    id_estudante    INTEGER      NOT NULL REFERENCES usuarios(id_usuario),
    id_disciplina   INTEGER      NOT NULL REFERENCES disciplinas(id_disciplina),
    id_documento    INTEGER      REFERENCES documentos_anexos(id_documento),
    mencao          VARCHAR(2)   NOT NULL CHECK (mencao IN ('SS', 'MS', 'MM', 'MI', 'II', 'SR')),
    semestre        VARCHAR(10)  NOT NULL,
    status          VARCHAR(20)  NOT NULL DEFAULT 'PENDENTE'
                        CHECK (status IN ('PENDENTE', 'APROVADO', 'REJEITADO')),
    justificativa   TEXT,
    data_cadastro   DATE         NOT NULL DEFAULT CURRENT_DATE,
    UNIQUE (id_estudante, id_disciplina, semestre)
);

CREATE TABLE inscricoes_turmas (
    id_inscricao  SERIAL PRIMARY KEY,
    id_estudante  INTEGER      NOT NULL REFERENCES usuarios(id_usuario),
    id_turma      INTEGER      NOT NULL REFERENCES turmas(id_turma),
    id_documento  INTEGER      REFERENCES documentos_anexos(id_documento),
    status        VARCHAR(20)  NOT NULL DEFAULT 'PENDENTE'
                  CHECK (status IN ('PENDENTE', 'APROVADA', 'REJEITADA')),
    justificativa TEXT,
    data_cadastro DATE         NOT NULL DEFAULT CURRENT_DATE,
    UNIQUE (id_estudante, id_turma)
);

CREATE TABLE agenda_slots (
    id_slot              SERIAL PRIMARY KEY,
    id_alocacao          INTEGER      NOT NULL REFERENCES alocacoes_monitores(id_alocacao),
    data_slot            DATE         NOT NULL,
    hora_inicio          TIME         NOT NULL,
    hora_fim             TIME         NOT NULL,
    local_atendimento    VARCHAR(120),
    modalidade           VARCHAR(20)  NOT NULL CHECK (modalidade IN ('PRESENCIAL', 'ONLINE', 'HIBRIDA')),
    reservado            BOOLEAN      NOT NULL DEFAULT FALSE,
    CHECK (hora_fim > hora_inicio)
);

CREATE TABLE sessoes_tutoria (
    id_sessao       SERIAL PRIMARY KEY,
    id_slot         INTEGER      NOT NULL UNIQUE REFERENCES agenda_slots(id_slot),
    id_estudante    INTEGER      NOT NULL REFERENCES usuarios(id_usuario),
    assunto         VARCHAR(180) NOT NULL,
    realizada       BOOLEAN      NOT NULL DEFAULT FALSE,
    data_registro   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE avaliacoes_tutoria (
    id_avaliacao    SERIAL PRIMARY KEY,
    id_sessao       INTEGER   NOT NULL REFERENCES sessoes_tutoria(id_sessao),
    id_estudante    INTEGER   NOT NULL REFERENCES usuarios(id_usuario),
    nota            INTEGER   NOT NULL CHECK (nota BETWEEN 1 AND 5),
    comentario      TEXT,
    data_avaliacao  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (id_sessao, id_estudante)
);

CREATE TABLE auditoria (
    id_auditoria SERIAL PRIMARY KEY,
    id_usuario   INTEGER   REFERENCES usuarios(id_usuario),
    acao         TEXT      NOT NULL,
    entidade     TEXT      NOT NULL,
    detalhes     TEXT,
    criado_em    TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- PERMISSOES
-- ============================================================

GRANT ALL ON ALL TABLES    IN SCHEMA public TO sigmon_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO sigmon_user;