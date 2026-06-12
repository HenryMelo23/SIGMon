# SIGMon - Sistema Integrado de Gestão de Monitoria

Aplicação web institucional para gestão de monitoria acadêmica do Departamento de Ciência da Computação da Universidade de Brasília.

O projeto usa Flask com templates Jinja2, CSS e JavaScript simples. Não há React, Angular, Vue nem SPA. A persistência atual é mockada em memória, com repositories desacoplados para facilitar a futura troca por PostgreSQL.

## Stack

- Python
- Flask
- Jinja2 Templates
- HTML, CSS e JavaScript simples
- Blueprints
- Services
- Repositories
- Models com dataclasses
- Mocks em memória

## Interface visual

A interface foi estilizada com identidade visual inspirada na UnB/CIC, usando verde institucional, azul profundo, branco, cinzas claros e detalhes dourados. O layout mantém uma proposta administrativa e acadêmica, com sidebar por perfil, header institucional, cards de dashboard, tabelas responsivas, badges de status e mensagens flash em formato de toast.

## Como rodar

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

Depois:

```bash
pip install -r requirements.txt
python run.py
```

Acesse:

```txt
http://localhost:5000
```

Se a porta 5000 já estiver ocupada, rode em outra porta:

```bash
PORT=5001 python run.py
```

No PowerShell:

```powershell
$env:PORT=5001; python run.py
```

## Usuários de teste

Todos usam a senha `123456`.

| Perfil | E-mail |
|---|---|
| Administrador | admin@unb.br |
| Professor | professor@unb.br |
| Estudante | estudante@unb.br |
| Monitor | monitor@unb.br |
| Financeiro | financeiro@unb.br |

Há também um usuário inativo (`inativo@unb.br`) para demonstrar bloqueio de login.

## Estrutura

```txt
app/
  models/          Entidades do domínio
  repositories/    Persistência mockada, substituível por PostgreSQL
  services/        Regras de negócio
  routes/          Blueprints Flask
  templates/       Telas Jinja2
  static/          CSS e JS
  mocks/           Dados simulados
  utils/           Permissões, decorators, validações e auditoria
sql/               Planejamento PostgreSQL
run.py             Entrada da aplicação
```

## Perfis e permissões

- Estudante: editais abertos, candidatura, agenda, sessões e avaliações.
- Monitor: alocação própria, criação de slots, sessões, frequência e avaliações recebidas.
- Professor: turmas, candidaturas, alocações, validação de frequência e relatórios.
- Administrador: cadastros, editais, candidaturas, alocações e visão geral.
- Financeiro: monitores ativos, dados bancários e frequências validadas.

Rotas sensíveis usam decorators de login e papel. Acesso direto por URL sem permissão retorna 403.

## Regras implementadas

- Usuário inativo não faz login.
- Estudante não se candidata duas vezes ao mesmo edital.
- Candidatura só é permitida em edital aberto.
- Candidatura nasce como `INSCRITA`.
- Professor/administrador alteram status de candidatura.
- Apenas candidatura `APROVADA` gera alocação.
- Dados bancários são restritos a financeiro/administrador.
- Slot reservado não pode ser reservado novamente.
- Reserva de slot cria sessão de tutoria.
- Frequência nasce não validada.
- Apenas professor valida frequência.
- Financeiro vê apenas frequências validadas.
- Avaliação só é criada para sessão realizada.
- Ações sensíveis registram auditoria simulada.

## Mocks e futura persistência

Os dados ficam em `app/mocks/mock_data.py`. Os repositories em `app/repositories/` são a fronteira de persistência. Para trocar por PostgreSQL, crie repositories concretos usando SQLAlchemy ou psycopg2 e preserve os métodos usados pelas services (`list_all`, `get_by_id`, `create`, `update`, `delete`).

O módulo `app/database/postgres_placeholder.py` marca o ponto de inicialização futura para conexão, pool, migrations e ORM.

## SQL planejado

A pasta `sql/` inclui:

- `estrutura_futura.sql`: tabelas, chaves, checks e índices.
- `triggers_planejadas.sql`: validações e auditoria.
- `views_planejadas.sql`: dashboards e visões financeiras.
- `procedures_planejadas.sql`: aprovação, alocação, folha e validações em lote.

## LGPD e auditoria

O sistema separa dados bancários e restringe acesso por perfil. A função `registrar_auditoria(usuario_id, acao, entidade, detalhes)` simula trilha de auditoria para acesso financeiro, aprovação/alteração de candidaturas e validação de frequência.
