from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

import hashlib
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel, EmailStr

from database import conectar
from tasks import criar_tarefa, listar_tarefas, concluir_tarefa, desmarcar_tarefa, excluir_tarefa

# =========================
# Config
# =========================
SECRET_KEY = "TROQUE_ESSA_CHAVE_POR_UMA_BEM_GRANDE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app = FastAPI(title="OrganizaPy API", version="1.0.0")

# CORS (ajuste se o frontend rodar em outra porta/domínio)
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
# =========================
# Schemas
# =========================
class RegisterIn(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class LoginIn(BaseModel):
    email: EmailStr
    senha: str

class TokenOut(BaseModel):
    token: str
    usuario: Dict[str, Any]

class TaskCreateIn(BaseModel):
    titulo: str
    descricao: Optional[str] = None

class TaskOut(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str] = None
    concluida: int

# =========================
# Helpers
# =========================
def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_email(email: str):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, email, senha FROM usuarios WHERE email = ?", (email,))
        return cursor.fetchone()
    finally:
        conexao.close()

def create_user(nome: str, email: str, senha_hash: str):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha_hash)
        )
        conexao.commit()
        return cursor.lastrowid
    finally:
        conexao.close()

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")


# =========================
# Routes
# =========================
@app.get("/health")
def health():
    return {"ok": True}

@app.post("/auth/register")
def register(data: RegisterIn):
    if not data.nome.strip() or not data.email.strip() or not data.senha.strip():
        raise HTTPException(status_code=400, detail="Campos obrigatórios ausentes")

    existing = get_user_by_email(data.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email já cadastrado")

    senha_hash = hash_senha(data.senha)
    user_id = create_user(data.nome.strip(), data.email.strip(), senha_hash)

    return {"ok": True, "id": user_id}

@app.post("/auth/login", response_model=TokenOut)
def login(data: LoginIn):
    user = get_user_by_email(data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    user_id, nome, email, senha_db = user
    if hash_senha(data.senha) != senha_db:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_access_token(
        data={"sub": str(user_id), "nome": nome},
        expires_delta=timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    )

    return {"token": token, "usuario": {"id": user_id, "nome": nome}}

@app.get("/tasks", response_model=List[TaskOut])
def get_tasks(user_id: int = Depends(get_current_user_id)):
    rows = listar_tarefas(user_id)
    # rows = (id, titulo, descricao, concluida, usuario_id)
    tasks = []
    for r in rows:
        tasks.append({"id": r[0], "titulo": r[1], "descricao": r[2], "concluida": r[3]})
    return tasks

@app.post("/tasks")
def add_task(data: TaskCreateIn, user_id: int = Depends(get_current_user_id)):
    titulo = data.titulo.strip()
    if not titulo:
        raise HTTPException(status_code=400, detail="Título é obrigatório")

    ok = criar_tarefa(titulo, user_id, data.descricao)
    if not ok:
        raise HTTPException(status_code=400, detail="Não foi possível criar tarefa")
    return {"ok": True}

@app.patch("/tasks/{task_id}/done")
def done_task(task_id: int, user_id: int = Depends(get_current_user_id)):
    ok = concluir_tarefa(task_id, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"ok": True}

@app.patch("/tasks/{task_id}/undone")
def undone_task(task_id: int, user_id: int = Depends(get_current_user_id)):
    ok = desmarcar_tarefa(task_id, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"ok": True}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, user_id: int = Depends(get_current_user_id)):
    ok = excluir_tarefa(task_id, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"ok": True}