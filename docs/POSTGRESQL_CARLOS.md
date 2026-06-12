# Guia para integração do SIGMon com PostgreSQL

Este documento explica como substituir a persistência mockada atual do SIGMon por PostgreSQL, mantendo a arquitetura já criada em Flask/Jinja2.

O objetivo é orientar a próxima etapa de desenvolvimento sem reescrever o sistema do zero.

## 1. Como o SIGMon funciona hoje

Atualmente o sistema não usa banco real.

Os dados ficam em memória no arquivo:

```txt
app/mocks/mock_data.py
```

Os repositories atuais herdam de:

```txt
app/repositories/base_repository.py
```

O fluxo atual é:

```txt
templates -> routes -> services -> repositories -> mock_data.py
```

Exemplo:

```txt
Tela de usuários
  -> usuario_routes.py
  -> UsuarioService
  -> UsuarioRepository
  -> lista USUARIOS em mock_data.py
```

Isso significa que:

- o sistema funciona para demonstração;
- os dados são alterados apenas em memória;
- ao reiniciar o Flask, os dados voltam ao estado inicial;
- ainda não existe persistência real.

## 2. Estratégia recomendada

A melhor estratégia é manter o desenho atual:

```txt
routes -> services -> repositories
```

E trocar apenas a camada de repository.

Ou seja:

- não reescrever templates;
- não reescrever rotas;
- não jogar regra de negócio dentro das rotas;
- não acessar banco diretamente nos templates;
- não acessar banco diretamente nas services, exceto se for inevitável.

O ideal é que as services continuem chamando métodos como:

```python
repo.list_all()
repo.get_by_id(id)
repo.create(data)
repo.update(id, data)
repo.delete(id)
```

Mas esses métodos passarão a consultar PostgreSQL em vez dos mocks.

## 3. Stack sugerida

Use:

- PostgreSQL;
- SQLAlchemy;
- Flask-SQLAlchemy;
- Flask-Migrate;
- psycopg2-binary;
- python-dotenv.

Instale:

```bash
pip install Flask-SQLAlchemy Flask-Migrate psycopg2-binary python-dotenv
```

Atualize o `requirements.txt`:

```txt
Flask-SQLAlchemy
Flask-Migrate
psycopg2-binary
python-dotenv
```

## 4. Criar o banco PostgreSQL

No PostgreSQL, crie um banco para o projeto:

```sql
CREATE DATABASE sigmon;
```

Crie um usuário específico para a aplicação:

```sql
CREATE USER sigmon_user WITH PASSWORD 'trocar_esta_senha';
GRANT ALL PRIVILEGES ON DATABASE sigmon TO sigmon_user;
```

Em ambiente local, a URL ficaria parecida com:

```txt
postgresql://sigmon_user:trocar_esta_senha@localhost:5432/sigmon
```

## 5. Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=trocar_por_uma_chave_segura
DATABASE_URL=postgresql://sigmon_user:trocar_esta_senha@localhost:5432/sigmon
FLASK_ENV=development
```

Não versionar `.env` se o projeto virar repositório Git público ou compartilhado.

Criar também um `.env.example`:

```env
SECRET_KEY=change-me
DATABASE_URL=postgresql://user:password@localhost:5432/sigmon
FLASK_ENV=development
```

## 6. Ajustar configuração Flask

Arquivo atual:

```txt
app/config.py
```

Sugestão:

```python
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "sigmon-dev-secret")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    APP_NAME = "SIGMon"

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## 7. Criar inicializador do banco

Criar:

```txt
app/database/db.py
```

Conteúdo:

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
```

Depois alterar:

```txt
app/__init__.py
```

Adicionar:

```python
from app.database.db import db, migrate
```

Dentro de `create_app()`:

```python
db.init_app(app)
migrate.init_app(app, db)
```

Exemplo:

```python
def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)
    return app
```

## 8. Criar models ORM

Hoje os models em:

```txt
app/models/
```

são `dataclasses`.

Para PostgreSQL com SQLAlchemy, existem duas opções:

### Opção A: substituir dataclasses por models SQLAlchemy

Mais simples para um projeto pequeno/médio.

Exemplo:

```python
from app.database.db import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True)
    id_departamento = db.Column(db.Integer, db.ForeignKey("departamentos.id_departamento"), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    matricula = db.Column(db.String(30), nullable=False)
    papel = db.Column(db.String(20), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    data_cadastro = db.Column(db.Date, nullable=False)
```

### Opção B: manter dataclasses e criar ORM separado

Mais organizado em arquitetura grande, mas dá mais trabalho.

Exemplo:

```txt
app/models/usuario.py              # entidade de domínio
app/database/orm/usuario_model.py  # tabela SQLAlchemy
```

Para o SIGMon, a opção A é suficiente e mais rápida.

## 9. Tabelas principais

As tabelas planejadas estão documentadas em:

```txt
sql/estrutura_futura.sql
sql/views_planejadas.sql
sql/triggers_planejadas.sql
sql/procedures_planejadas.sql
```

Entidades principais:

- departamentos;
- usuarios;
- disciplinas;
- turmas;
- editais;
- candidaturas;
- alocacoes_monitores;
- dados_bancarios;
- documentos_anexos;
- agenda_slots;
- sessoes_tutoria;
- registros_frequencia;
- avaliacoes_tutoria.

## 10. Repositories com PostgreSQL

Hoje um repository funciona assim:

```python
class UsuarioRepository(BaseRepository):
    dataset_name = "usuarios"
    id_field = "id_usuario"

    def find_by_email(self, email):
        return next((u for u in self.items if u.email.lower() == email.lower()), None)
```

Com PostgreSQL, ele deve ficar mais ou menos assim:

```python
from app.models.usuario import Usuario
from app.database.db import db


class UsuarioRepository:
    def list_all(self):
        return Usuario.query.order_by(Usuario.nome.asc()).all()

    def get_by_id(self, item_id):
        if item_id is None:
            return None
        return Usuario.query.get(int(item_id))

    def find_by_email(self, email):
        return Usuario.query.filter(db.func.lower(Usuario.email) == email.lower()).first()

    def list_by_role(self, papel):
        return Usuario.query.filter_by(papel=papel).order_by(Usuario.nome.asc()).all()

    def create(self, data):
        usuario = Usuario(**data)
        db.session.add(usuario)
        db.session.commit()
        return usuario

    def update(self, item_id, data):
        usuario = self.get_by_id(item_id)
        if not usuario:
            return None
        for key, value in data.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)
        db.session.commit()
        return usuario

    def delete(self, item_id):
        usuario = self.get_by_id(item_id)
        if not usuario:
            return False
        db.session.delete(usuario)
        db.session.commit()
        return True
```

O importante é manter os mesmos nomes de métodos usados pelas services.

## 11. Migrações

Depois de configurar Flask-Migrate:

```bash
flask db init
flask db migrate -m "estrutura inicial"
flask db upgrade
```

Se o comando `flask` não encontrar a app:

No Windows PowerShell:

```powershell
$env:FLASK_APP="run.py"
flask db init
flask db migrate -m "estrutura inicial"
flask db upgrade
```

Linux/Mac:

```bash
export FLASK_APP=run.py
flask db init
flask db migrate -m "estrutura inicial"
flask db upgrade
```

## 12. Popular dados iniciais

Os mocks atuais podem virar seed.

Criar:

```txt
app/database/seeds.py
```

Exemplo:

```python
from app.database.db import db
from app.models.usuario import Usuario


def seed_usuarios():
    if Usuario.query.filter_by(email="admin@unb.br").first():
        return

    admin = Usuario(
        id_departamento=1,
        nome="Ana Beatriz Martins",
        email="admin@unb.br",
        matricula="ADM001",
        papel="ADMINISTRADOR",
        senha_hash="123456",
        ativo=True,
        data_cadastro="2026-01-10",
    )

    db.session.add(admin)
    db.session.commit()
```

Depois criar um comando Flask para executar seeds.

## 13. Cuidado com senhas

Hoje a senha está mockada como texto simples:

```txt
123456
```

Para banco real, usar hash.

Com Werkzeug:

```python
from werkzeug.security import generate_password_hash, check_password_hash

senha_hash = generate_password_hash("123456")
check_password_hash(usuario.senha_hash, senha_digitada)
```

Alterar o `AuthService` para comparar usando `check_password_hash`.

## 14. Dados bancários e LGPD

A tabela `dados_bancarios` deve receber atenção especial.

Recomendações:

- restringir acesso apenas a `FINANCEIRO` e `ADMINISTRADOR`;
- manter auditoria de acesso;
- evitar expor dados bancários em logs;
- considerar criptografia de campos sensíveis;
- mascarar agência/conta em telas onde o dado completo não for necessário.

Exemplo de mascaramento:

```python
def mascarar_conta(conta):
    if not conta:
        return "-"
    return "***" + conta[-3:]
```

## 15. Auditoria

Hoje existe auditoria simulada em:

```txt
app/utils/audit.py
```

No PostgreSQL, criar tabela:

```sql
CREATE TABLE auditoria (
  id_auditoria SERIAL PRIMARY KEY,
  id_usuario INTEGER REFERENCES usuarios(id_usuario),
  acao TEXT NOT NULL,
  entidade TEXT NOT NULL,
  detalhes TEXT,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);
```

Depois trocar `registrar_auditoria` para gravar no banco.

## 16. Ordem prática de implementação

Sugestão de ordem para evitar quebrar o sistema:

1. Instalar dependências.
2. Configurar `.env`.
3. Criar `app/database/db.py`.
4. Inicializar `db` e `migrate` no `create_app`.
5. Converter/criar models SQLAlchemy.
6. Criar a primeira migration.
7. Rodar `flask db upgrade`.
8. Migrar `UsuarioRepository`.
9. Ajustar `AuthService` para usar senha com hash.
10. Criar seed de usuários.
11. Testar login.
12. Migrar repositories restantes um por vez.
13. Testar cada tela após migrar seu repository.
14. Trocar auditoria simulada por auditoria em tabela.
15. Revisar permissões e dados sensíveis.

## 17. Ordem sugerida dos repositories

Migrar nesta ordem:

1. `DepartamentoRepository`
2. `UsuarioRepository`
3. `DisciplinaRepository`
4. `TurmaRepository`
5. `EditalRepository`
6. `CandidaturaRepository`
7. `AlocacaoRepository`
8. `AgendaRepository`
9. `SessaoRepository`
10. `FrequenciaRepository`
11. `AvaliacaoRepository`
12. `DadosBancariosRepository`
13. `FinanceiroRepository`

Essa ordem respeita dependências naturais entre as entidades.

## 18. Testes manuais mínimos após integrar

Testar:

- login com usuário ativo;
- bloqueio de usuário inativo;
- listagem de editais;
- candidatura de estudante;
- bloqueio de candidatura duplicada;
- alteração de status por professor/admin;
- criação de alocação apenas com candidatura aprovada;
- criação de slot por monitor;
- reserva de slot por estudante;
- registro de frequência por monitor;
- validação de frequência por professor;
- acesso financeiro apenas por financeiro/admin;
- auditoria ao acessar financeiro;
- persistência após reiniciar o Flask.

## 19. Checklist final

Antes de considerar PostgreSQL integrado:

- [ ] `DATABASE_URL` configurada;
- [ ] models SQLAlchemy criados;
- [ ] migrations criadas;
- [ ] `flask db upgrade` executado;
- [ ] seeds criadas;
- [ ] login usando dados do banco;
- [ ] repositories usando banco;
- [ ] mocks removidos do fluxo principal;
- [ ] dados persistem após reiniciar servidor;
- [ ] auditoria gravando em banco;
- [ ] dados bancários protegidos por permissão;
- [ ] README atualizado com instruções do PostgreSQL.

## 20. Observação importante

Não misture duas estratégias no meio do caminho.

Evite deixar algumas telas usando PostgreSQL e outras usando mocks sem uma razão clara. Durante a migração incremental, isso pode acontecer temporariamente, mas documente o que já foi migrado e o que ainda depende de `mock_data.py`.

O objetivo final é:

```txt
templates -> routes -> services -> repositories -> PostgreSQL
```

E não mais:

```txt
templates -> routes -> services -> repositories -> mock_data.py
```
