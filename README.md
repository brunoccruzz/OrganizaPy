# OrganizaPy ✅
Gerenciador de tarefas com **autenticação** e **persistência em SQLite**.

- Backend: **Python + FastAPI + SQLite**
- Frontend: **React (Vite) + UI Shadcn + Rich design (Lovable)**

---

## 📁 Estrutura (sugestão)
Você terá duas pastas separadas:


IdeaProjects/
OrganizaPy/ # backend python
.venv/
organiza-python/
api.py
auth.py
tasks.py
database.py
models.py
organizapy.db
organizapy-web/ # frontend lovable
src/
package.json
.env


> Importante: **não misture** o frontend dentro da pasta do backend.

---

## ✅ Requisitos
- Python 3.x
- Node.js + npm
- SQLite (já vem junto com Python na maioria dos casos)

---

# 🚀 Rodando o BACKEND (FastAPI)

## 1) Entrar no backend
```bash
cd ~/IdeaProjects/OrganizaPy/organiza-python
2) Ativar o venv

O venv fica um nível acima:

source ../.venv/bin/activate

Se tudo certo, aparecerá algo assim:

(.venv) ...
3) Instalar dependências no venv (uma vez)
pip install fastapi uvicorn "python-jose[cryptography]" python-multipart email-validator
4) Subir o servidor
uvicorn api:app --reload --port 8000

✅ Testes:

Health: http://localhost:8000/health

Swagger: http://localhost:8000/docs

🌐 Rodando o FRONTEND (Lovable)
1) Entrar na pasta do front
cd ~/IdeaProjects/organizapy-web
2) Instalar dependências (uma vez)
npm install
3) Configurar URL do backend (VITE_API_URL)

Crie/edite o arquivo .env na raiz do frontend:

nano .env

Conteúdo:

VITE_API_URL=http://localhost:8000

Se você mudar o .env, reinicie o npm run dev.

4) Rodar o front
npm run dev

O terminal mostrará a URL local, por exemplo:

http://localhost:8080/ (pode variar)

⚠️ CORS (muito importante)

Se o frontend rodar em http://localhost:8080, o backend precisa aceitar essa origem.

No api.py, configure:

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Depois reinicie o backend (Ctrl+C e rode uvicorn de novo).

🧪 Fluxo de uso

Abra o frontend (URL do npm run dev)

Faça Registro

Faça Login

No Dashboard:

Criar tarefa

Listar tarefas

Concluir / Desmarcar

Excluir

🛠️ Troubleshooting
“Failed to fetch” no Registro/Login

Quase sempre é 1 destes:

Backend não está rodando

VITE_API_URL errado

CORS não inclui a porta do frontend

✅ Check rápido:

curl -i http://localhost:8000/health
cat .env
“uvicorn: comando não encontrado”

Você esqueceu de ativar o venv:

source ../.venv/bin/activate
“Could not import module api”

Você rodou o uvicorn fora da pasta onde está o api.py.
Rode dentro de:

cd ~/IdeaProjects/OrganizaPy/organiza-python
uvicorn api:app --reload --port 8000
📌 Tecnologias

Python

FastAPI

SQLite

JWT

React + Vite

Tailwind / shadcn-ui

Git / GitHub
