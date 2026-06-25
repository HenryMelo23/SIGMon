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
DROP TABLE IF EXISTS registros_frequencia   CASCADE;
DROP TABLE IF EXISTS sessoes_tutoria        CASCADE;
DROP TABLE IF EXISTS agenda_slots           CASCADE;
DROP TABLE IF EXISTS documentos_anexos      CASCADE;
DROP TABLE IF EXISTS dados_bancarios        CASCADE;
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
                        papel IN ('ESTUDANTE', 'MONITOR', 'PROFESSOR', 'ADMINISTRADOR', 'FINANCEIRO')
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
    dias        VARCHAR(10)  NOT NULL,
    turno       CHAR(1)      NOT NULL CHECK (turno IN ('M', 'T', 'N')),
    ativo       BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE TABLE turmas (
    id_turma        SERIAL PRIMARY KEY,
    id_disciplina   INTEGER      NOT NULL REFERENCES disciplinas(id_disciplina),
    id_professor    INTEGER      NOT NULL REFERENCES usuarios(id_usuario),
    semestre        VARCHAR(10)  NOT NULL,
    codigo_turma    VARCHAR(20)  NOT NULL,
    tipo_turma      VARCHAR(20)  NOT NULL CHECK (tipo_turma IN ('TEORICA', 'PRATICA')),
    id_horario      INTEGER      REFERENCES horarios(id_horario),
    sala            VARCHAR(80),
    UNIQUE (id_disciplina, semestre, codigo_turma)
);

CREATE TABLE editais (
    id_edital         SERIAL PRIMARY KEY,
    id_departamento   INTEGER       NOT NULL REFERENCES departamentos(id_departamento),
    titulo            VARCHAR(180)  NOT NULL,
    descricao         TEXT,
    data_inicio       DATE          NOT NULL,
    data_fim          DATE          NOT NULL,
    quantidade_vagas  INTEGER       NOT NULL CHECK (quantidade_vagas > 0),
    nota_minima       NUMERIC(4,2)  NOT NULL DEFAULT 7.00 CHECK (nota_minima BETWEEN 0 AND 10),
    CHECK (data_fim >= data_inicio)
);

CREATE TABLE candidaturas (
    id_candidatura  SERIAL PRIMARY KEY,
    id_edital       INTEGER      NOT NULL REFERENCES editais(id_edital),
    id_estudante    INTEGER      NOT NULL REFERENCES usuarios(id_usuario),
    data_inscricao  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ira             NUMERIC(4,2) CHECK (ira BETWEEN 0 AND 5),
    nota_disciplina NUMERIC(4,2) CHECK (nota_disciplina BETWEEN 0 AND 10),
    status          VARCHAR(20)  NOT NULL DEFAULT 'INSCRITA' CHECK (
                        status IN ('INSCRITA', 'EM_ANALISE', 'APROVADA', 'REPROVADA', 'CANCELADA')
                    ),
    UNIQUE (id_edital, id_estudante)
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

CREATE TABLE dados_bancarios (
    id_dado_bancario SERIAL PRIMARY KEY,
    id_usuario       INTEGER      NOT NULL UNIQUE REFERENCES usuarios(id_usuario),
    banco            VARCHAR(80)  NOT NULL,
    agencia          VARCHAR(20)  NOT NULL,
    conta            VARCHAR(30)  NOT NULL,
    tipo_conta       VARCHAR(20)  CHECK (tipo_conta IN ('CORRENTE', 'POUPANCA')),
    chave_pix        VARCHAR(150),
    atualizado_em    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Armazena documentos binarios (PDF, imagens) vinculados a usuarios, editais ou candidaturas.
-- O campo conteudo usa BYTEA para armazenar o arquivo diretamente no banco.
CREATE TABLE documentos_anexos (
    id_documento    SERIAL PRIMARY KEY,
    id_usuario      INTEGER       REFERENCES usuarios(id_usuario),
    id_edital       INTEGER       REFERENCES editais(id_edital),
    id_candidatura  INTEGER       REFERENCES candidaturas(id_candidatura),
    nome_arquivo    VARCHAR(180)  NOT NULL,
    tipo_documento  VARCHAR(60)   NOT NULL,
    mime_type       VARCHAR(100)  NOT NULL,
    conteudo        BYTEA,
    data_upload     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
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
    observacoes     TEXT,
    realizada       BOOLEAN      NOT NULL DEFAULT FALSE,
    data_registro   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE registros_frequencia (
    id_frequencia          SERIAL PRIMARY KEY,
    id_alocacao            INTEGER      NOT NULL REFERENCES alocacoes_monitores(id_alocacao),
    data_atividade         DATE         NOT NULL,
    horas                  NUMERIC(4,2) NOT NULL CHECK (horas > 0),
    descricao              TEXT         NOT NULL,
    validado               BOOLEAN      NOT NULL DEFAULT FALSE,
    id_professor_validador INTEGER      REFERENCES usuarios(id_usuario)
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