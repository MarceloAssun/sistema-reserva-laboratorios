# 🚀 Guia de Deploy no PythonAnywhere

Este documento fornece um passo a passo detalhado para colocar a aplicação no ar no PythonAnywhere.

## ⚠️ Pré-requisitos

- Conta GitHub com o repositório público
- Conta PythonAnywhere (gratuita em https://www.pythonanywhere.com)
- Terminal/Bash (PythonAnywhere fornece)

## 📋 Resumo do Processo

1. Criar conta PythonAnywhere
2. Abrir Bash Console
3. Clonar repositório GitHub
4. Criar virtualenv
5. Instalar requirements.txt
6. Configurar .env
7. Executar migrations
8. Executar seed_demo (dados de demonstração)
9. Coletar estáticos
10. Configurar Web App
11. Configurar arquivo WSGI
12. Testar aplicação

---

## 🔧 PASSO 1: Criar Conta PythonAnywhere

1. Acesse https://www.pythonanywhere.com
2. Clique em "Pricing"
3. Escolha o plano gratuito ("Beginner")
4. Clique "Sign up"
5. Preencha o formulário com:
   - **Username**: Escolha um nome (será sua URL: `SEU_USUARIO.pythonanywhere.com`)
   - **Email**: Seu e-mail
   - **Password**: Senha segura
6. Confirme seu e-mail
7. Faça login

---

## 💻 PASSO 2: Abrir Bash Console

1. Após fazer login, clique em **"Bash"** no menu superior
2. Um terminal irá abrir
3. Você estará em `/home/SEU_USUARIO`

---

## 📥 PASSO 3: Clonar Repositório GitHub

No Bash Console, execute:

```bash
git clone https://github.com/SEU_USUARIO/sistema-reserva-laboratorios.git
cd sistema-reserva-laboratorios
```

Verifique que foi clonado:

```bash
ls -la
```

Deve mostrar `backend/`, `frontend/`, `README.md`, etc.

---

## 🐍 PASSO 4: Criar Virtualenv

No mesmo diretório (`/home/SEU_USUARIO/sistema-reserva-laboratorios`), execute:

```bash
python3 -m venv venv
source venv/bin/activate
```

Seu terminal agora deve mostrar `(venv)` no início da linha.

---

## 📦 PASSO 5: Instalar requirements.txt

```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

Aguarde a instalação terminar (pode levar 2-3 minutos).

---

## ⚙️ PASSO 6: Configurar .env

Ainda no diretório `backend/`, crie o arquivo `.env`:

```bash
nano .env
```

Cole o seguinte conteúdo:

```env
SECRET_KEY=gerar-chave-segura
DEBUG=False
ALLOWED_HOSTS=127.0.0.1,localhost,SEU_USUARIO.pythonanywhere.com
DB_ENGINE=sqlite
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
CORS_ALLOWED_ORIGINS=https://SEU_USUARIO.pythonanywhere.com
DEMO_PASSWORD=demo12345
```

**Importantes**:
- Substitua `SEU_USUARIO` pelo seu username real do PythonAnywhere
- Para gerar uma `SECRET_KEY` segura, você pode usar:

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copie a saída e substitua `gerar-chave-segura` por ela.

Para salvar no nano:
1. Pressione `Ctrl + X`
2. Digite `Y` para sim
3. Pressione `Enter` para confirmar o nome

---

## 🗄️ PASSO 7: Executar Migrations

Ainda no Bash e no diretório `backend/`:

```bash
python manage.py migrate
```

Esperado: `Running migrations...` e depois `OK`.

---

## 🌱 PASSO 8: Criar Dados de Demonstração

```bash
python manage.py seed_demo
```

Isso cria:
- Grupos (Alunos, Professores, Administradores)
- Usuários: `aluno`, `professor`, `admin` (todos com senha `demo12345`)
- Laboratórios de exemplo

---

## 📂 PASSO 9: Coletar Arquivos Estáticos

```bash
python manage.py collectstatic --noinput
```

Esperado: Arquivos copiados para `staticfiles/`

Verifique:

```bash
ls -la staticfiles/ | head -20
```

Deve mostrar arquivos de admin, etc.

---

## 🌐 PASSO 10: Configurar Web App no Painel PythonAnywhere

1. Volte para o navegador
2. Clique na aba **"Web"** no menu superior
3. Clique em **"Add a new web app"**
4. Escolha:
   - **Python version**: Python 3.10 (ou similar)
   - **Framework**: Django
5. PythonAnywhere vai criar uma configuração padrão

---

## 🔧 PASSO 11: Configurar Arquivo WSGI

1. Na aba **Web**, você verá uma seção **"Code"**
2. Clique no arquivo WSGI (algo como `/var/www/SEU_USUARIO_pythonanywhere_com_wsgi.py`)
3. Será aberto um editor
4. **Apague todo o conteúdo** e cole:

```python
import os
import sys
from pathlib import Path

# Caminho para a pasta do projeto
project_dir = Path("/home/SEU_USUARIO/sistema-reserva-laboratorios/backend")
sys.path.insert(0, str(project_dir))

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

# Virtualenv
virtualenv_dir = Path("/home/SEU_USUARIO/sistema-reserva-laboratorios/venv")
os.environ["PATH"] = str(virtualenv_dir / "bin") + ":" + os.environ.get("PATH", "")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**IMPORTANTE**: Substitua `SEU_USUARIO` pelo seu username real.

Salve o arquivo (Ctrl+S ou clique em Save).

---

## 📁 PASSO 12: Configurar Static Files

Voltando na aba **Web**:

1. Procure pela seção **"Static files"**
2. Clique em **"Add a new static files mapping"**
3. Preencha:
   - **URL**: `/static/`
   - **Directory**: `/home/SEU_USUARIO/sistema-reserva-laboratorios/backend/staticfiles`

Clique em "Save" ou confirme.

---

## ♻️ PASSO 13: Recarregar a Aplicação

Ainda na aba **Web**:

1. Procure pelo botão verde de **"Reload"** (ou "Reload Web App")
2. Clique nele
3. Aguarde alguns segundos

---

## 🧪 PASSO 14: Testar a Aplicação

Abra uma nova aba do navegador e acesse:

```
https://SEU_USUARIO.pythonanywhere.com
```

**Esperado**:
- A página carregar
- Se houver erro, verifique os logs

### Acessar Logs

Na aba **Web**, procure por **"Log files"** e clique em **"Error log"** para ver problemas.

---

## 🔐 PASSO 15: Acessar Django Admin

Acesse:

```
https://SEU_USUARIO.pythonanywhere.com/admin
```

Faça login com:
- **Username**: `admin`
- **Password**: `demo12345`

---

## ✅ Verificação de Sucesso

Se tudo funcionou:

- ✅ URL pública acessível
- ✅ Admin funciona
- ✅ Arquivos estáticos carregam (CSS/JavaScript)
- ✅ Database funciona
- ✅ Usuários demo criados

---

## 🐛 Troubleshooting

### Erro: "Módulo config não encontrado"

**Causa**: PYTHONPATH incorreto

**Solução**: Verifique `sys.path.insert(0, ...)` no arquivo WSGI aponta para `backend/`

### Erro: "StaticFilesStorage" ou arquivos estáticos não carregam

**Causa**: Caminhos de static files incorretos

**Solução**:
1. Re-execute: `python manage.py collectstatic --noinput`
2. Verifique em Web > Static files se aponta para `staticfiles/` correto

### Erro: "Internal Server Error"

**Solução**:
1. Vá para Web > Error log
2. Leia a mensagem de erro
3. Corrija o problema localmente
4. Faça `git push`
5. No Bash do PythonAnywhere, faça `git pull` dentro do projeto
6. Recarregue a aplicação

### Erro: Database locked (SQLite)

**Causa**: Múltiplas requisições simultâneas em SQLite

**Solução**: É raro, mas se ocorrer:
1. Espere alguns minutos
2. Recarregue a aplicação
3. Se persistir, considere migrar para PostgreSQL (futuro)

---

## 🔄 Atualizações Futuras

Para atualizar a aplicação depois:

1. No seu computador local, faça mudanças
2. Execute `git commit -m "mensagem"`
3. Execute `git push`
4. No Bash do PythonAnywhere (dentro do projeto):
   ```bash
   git pull
   source venv/bin/activate
   cd backend
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
5. Na aba Web, clique em "Reload"

---

## 📞 Suporte Adicional

- PythonAnywhere Help: https://help.pythonanywhere.com/
- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/

---

## ✨ Pronto!

Sua aplicação deve estar no ar em:

```
https://SEU_USUARIO.pythonanywhere.com
```

Demonstre para seu orientador! 🎉
