# Sistema de Reserva de Laboratórios

Plataforma web para consulta, solicitação e gerenciamento de reservas de laboratórios acadêmicos.

## 📋 Sobre o projeto

Centralizar o processo de reserva de laboratórios, reduzir conflitos de horário e oferecer um histórico consultável para alunos, professores e administradores.

Esta versão é um **protótipo demonstrável** para apresentação ao orientador.

## 🛠️ Tecnologias

### Backend
- **Python** 3.12+
- **Django** 6.0.8
- **Django REST Framework** 3.16.1
- **Autenticação**: JWT (djangorestframework-simplejwt)
- **Banco de Dados**: SQLite (local/demo) | PostgreSQL (produção)

### Frontend
- **React.js** 18.3.1
- **Vite** 6.3.5
- **Axios** 1.11.0
- **React Router** 6.30.1

### DevOps
- **Git/GitHub** para controle de versão
- **PythonAnywhere** para hospedagem (demo)

## 📦 Requisitos

- Python 3.12+
- Node.js 18+ (para frontend)
- Git
- pip e npm (gerenciadores de pacotes)

## 🚀 Instalação Local

### 1. Clonar repositório

```bash
git clone https://github.com/SEU_USUARIO/sistema-reserva-laboratorios.git
cd sistema-reserva-laboratorios
```

### 2. Preparar Backend

#### 2.1 Criar ambiente virtual

```bash
cd backend
python -m venv venv
```

**Ativar ambiente virtual**:

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```

- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

#### 2.2 Instalar dependências

```bash
pip install -r requirements.txt
```

#### 2.3 Configurar variáveis de ambiente

```bash
# Copiar exemplo
cp .env.example .env

# Editar .env com suas configurações (já vem pré-configurado para SQLite)
# Não altere nada se for usar localmente
```

**Arquivo `.env`** já deverá ter:
```env
SECRET_KEY=demo-secret-key-para-apresentacao
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_ENGINE=sqlite
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
DEMO_PASSWORD=demo12345
```

#### 2.4 Executar migrações

```bash
python manage.py migrate
```

#### 2.5 Criar dados de demonstração

```bash
python manage.py seed_demo
```

Cria automaticamente:
- **Grupos**: Alunos, Professores, Administradores
- **Usuários demo**:
  - `aluno` / `demo12345` (perfil Aluno)
  - `professor` / `demo12345` (perfil Professor)
  - `admin` / `demo12345` (perfil Administrador + Staff)
- **Laboratórios demo**: 3 laboratórios de exemplo

#### 2.6 Executar servidor Django

```bash
python manage.py runserver
```

Backend estará disponível em: `http://localhost:8000`

- **Admin**: `http://localhost:8000/admin`
- **API**: `http://localhost:8000/api/`

### 3. Preparar Frontend

#### 3.1 Instalar dependências

```bash
cd ../frontend
npm install
```

#### 3.2 Executar dev server

```bash
npm run dev
```

Frontend estará disponível em: `http://localhost:5173`

---

## 🧪 Testes Locais

### Verificar configuração do Django

```bash
cd backend
python manage.py check
```

Esperado: `System check identified no issues (0 silenced).`

### Coletar arquivos estáticos

```bash
python manage.py collectstatic --noinput
```

Esperado: Arquivos copiados para `backend/staticfiles/`

---

## 👤 Perfis de Usuário

O sistema utiliza o modelo padrão de `User` do Django com diferenciação por grupos:

- **Aluno**: Pode visualizar laboratórios e fazer reservas
- **Professor**: Pode visualizar, fazer e aprovar/rejeitar reservas
- **Administrador**: Acesso total (Django Admin + API completa)

---

## 📁 Estrutura do Projeto

```
sistema-reserva-laboratorios/
├── backend/
│   ├── config/                 # Configurações do Django
│   │   ├── settings.py         # Configurações principais
│   │   ├── urls.py             # Rotas principais
│   │   ├── wsgi.py             # WSGI para produção
│   ├── contas/                 # Autenticação e usuários
│   │   ├── management/commands/
│   │   │   └── seed_demo.py    # Command para criar dados demo
│   │   ├── views.py
│   │   ├── serializers.py
│   ├── laboratorios/           # Gerenciamento de laboratórios
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   ├── reservas/               # Gerenciamento de reservas
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   ├── db.sqlite3              # Banco de dados (SQLite)
│   ├── manage.py               # CLI do Django
│   ├── requirements.txt         # Dependências Python
│   └── staticfiles/            # Arquivos estáticos coletados
├── frontend/
│   ├── src/
│   │   ├── components/         # Componentes React
│   │   ├── pages/              # Páginas da aplicação
│   │   ├── services/           # Chamadas à API
│   │   └── contexts/           # Context API (autenticação)
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── .env.example                # Variáveis de ambiente (template)
├── .gitignore                  # Arquivos ignorados pelo Git
├── README.md                   # Este arquivo
└── DEPLOY.md                   # Guia de deploy no PythonAnywhere
```

---

## 🔐 Segurança

### Variáveis de ambiente

Todas as configurações sensíveis (SECRET_KEY, senhas, hosts) são carregadas do arquivo `.env`, que **não é enviado ao GitHub** (incluído em `.gitignore`).

### Para desenvolvimento local

O arquivo `.env` já vem pré-configurado. Apenas execute os comandos de instalação acima.

### Para produção (PythonAnywhere)

Veja instruções em [DEPLOY.md](DEPLOY.md).

---

## 📚 Comandos Úteis

### Backend

```bash
# Entrar na pasta
cd backend

# Ativar ambiente virtual
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows

# Executar migrações
python manage.py migrate

# Criar dados de demonstração
python manage.py seed_demo

# Executar servidor
python manage.py runserver

# Verificar problemas de configuração
python manage.py check

# Coletar arquivos estáticos
python manage.py collectstatic --noinput
```

### Frontend

```bash
# Entrar na pasta
cd frontend

# Instalar dependências
npm install

# Executar dev server
npm run dev

# Build para produção
npm run build
```

---

## 🌐 Dados de Demonstração

O comando `python manage.py seed_demo` cria automaticamente:

**Usuários**:
| Username | Grupo | Senha | Email |
|----------|-------|-------|-------|
| aluno | Aluno | demo12345 | aluno@demo.local |
| professor | Professor | demo12345 | professor@demo.local |
| admin | Administrador | demo12345 | admin@demo.local |

**Laboratórios**:
- Laboratório de Informática 01 (capacidade: 30, bloco A)
- Laboratório de Informática 02 (capacidade: 25, bloco A)
- Laboratório de Eletrônica (capacidade: 20, bloco B)

---

## 🚀 Deploy no PythonAnywhere

Para hospedar esta aplicação gratuitamente no PythonAnywhere, siga o guia em [DEPLOY.md](DEPLOY.md).

Resumo:
1. Criar conta em PythonAnywhere
2. Clonar repositório
3. Criar virtualenv
4. Instalar dependências
5. Configurar variáveis de ambiente
6. Executar migrações e collectstatic
7. Configurar Web App
8. Testar URL pública

---

## 📝 Licença

[Adicionar licença conforme necessário]

---

## 👨‍💼 Autor

Desenvolvido para TCC (Trabalho de Conclusão de Curso)

---

## 🤝 Suporte

Em caso de dúvidas sobre instalação ou deploy, consulte:
- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- PythonAnywhere Help: https://help.pythonanywhere.com/

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Copie o arquivo de ambiente:

```bash
copy ..\.env.example .env
```

Ajuste `SECRET_KEY`, `DEBUG` e as credenciais do banco. Nunca versionar o arquivo `.env`.

### PostgreSQL

Crie um banco, por exemplo `reserva_labs`, e preencha no `.env`:

```
DB_ENGINE=postgres
DB_NAME=reserva_labs
DB_USER=postgres
DB_PASSWORD=sua-senha
DB_HOST=localhost
DB_PORT=5432
```

### Fallback SQLite (somente desenvolvimento local)

Se o PostgreSQL ainda não estiver disponível na máquina:

```
DB_ENGINE=sqlite
```

O ambiente oficial do TCC permanece PostgreSQL.

## Migrations e dados de demonstração

```bash
python manage.py migrate
python manage.py seed_demo
```

O comando `seed_demo` cria:

- grupos `Alunos`, `Professores` e `Administradores`
- usuários `aluno`, `professor` e `admin`
- laboratórios de Informática 01, Informática 02 e Eletrônica

A senha desses usuários vem de `DEMO_PASSWORD` no `.env` (valor de exemplo em `.env.example`). Troque essa senha em qualquer ambiente compartilhado.

## Superusuário extra (opcional)

```bash
python manage.py createsuperuser
```

O Django Admin permanece disponível em `/admin/`.

## Executar a API

```bash
python manage.py runserver
```

API em `http://127.0.0.1:8000/api/`.

Principais rotas:

- `POST /api/login/`
- `POST /api/refresh/`
- `POST /api/logout/`
- `GET /api/me/`
- `GET /api/dashboard/`
- `GET/POST/PUT/PATCH /api/laboratorios/`
- `GET /api/laboratorios/{id}/disponibilidade/?data=YYYY-MM-DD`
- `GET/POST/PATCH /api/reservas/`
- `POST /api/reservas/{id}/aprovar/`
- `POST /api/reservas/{id}/rejeitar/`
- `POST /api/reservas/{id}/cancelar/`
- `GET /api/usuarios/`

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Interface em `http://localhost:5173`.

O Axios usa `http://127.0.0.1:8000/api` por padrão. Para alterar:

```
VITE_API_URL=http://127.0.0.1:8000/api
```

em `frontend/.env`.

## Testes do backend

```bash
cd backend
python manage.py test
```

Os testes usam SQLite em memória de execução (`manage.py test`), independentemente do PostgreSQL.

## Regras principais

1. Somente professor solicita reserva.
2. A solicitação nasce como `PENDENTE`.
3. Somente administrador aprova ou rejeita.
4. Não podem existir duas reservas `APROVADA` sobrepostas no mesmo laboratório e data.
5. Laboratório inativo não pode ser reservado.
6. Cancelamento é lógico (`CANCELADA`); o registro permanece no banco.
7. Aluno apenas consulta laboratórios e disponibilidade.
8. Histórico vem das próprias reservas; não existe model `Relatorio`.

## Roteiro de demonstração

1. Login como `aluno` — consultar laboratórios e disponibilidade.
2. Login como `professor` — criar uma reserva e vê-la como Pendente.
3. Login como `admin` — aprovar a solicitação.
4. Login novamente como `professor` — status Aprovada.
5. Consultar disponibilidade — o horário deve aparecer ocupado.
6. Criar outra reserva sobreposta e tentar aprová-la — a API deve recusar o conflito.
