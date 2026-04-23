import os
import psutil
import requests
from agente import ejecutar_agente_auditor
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt

import tablas
from database import engine, get_db

# Crear las tablas en la BD si no existen
tablas.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DeepCheck AI API")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de Seguridad
SECRET_KEY = os.getenv("JWT_SECRET", "super_secret_key_fallback")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

# --- Esquemas de Pydantic ---
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class ChatRequest(BaseModel):
    message: str
    session_id: int | None = None
    model: str = "qwen2.5:7b"

# --- Funciones Auxiliares ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# --- ENDPOINTS (Con Doble Decorador para fix de Nginx) ---

@app.post("/register")
@app.post("/api/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(tablas.User).filter((tablas.User.email == user.email) | (tablas.User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario o email ya registrado")
    
    hashed_pwd = get_password_hash(user.password)
    new_user = tablas.User(username=user.username, email=user.email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "Usuario creado exitosamente"}

@app.post("/login")
@app.post("/api/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(tablas.User).filter(tablas.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    
    access_token = create_access_token(data={"sub": db_user.email, "is_admin": db_user.is_admin, "user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer", "is_admin": db_user.is_admin}

@app.post("/chat")
@app.post("/api/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # Lógica simplificada de sesión (asumiendo que el JWT inyecta el user_id en la ruta real)
    # 1. Crear sesión si es null
    session_id = request.session_id
    if not session_id:
        new_session = tablas.ChatSession(user_id=1, title=request.message[:30]) # Mock de user_id=1
        db.add(new_session)
        db.commit()
        session_id = new_session.id

    # 2. Guardar mensaje del usuario
    user_msg = tablas.ChatMessage(session_id=session_id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    # 3. Consultar a Ollama
    payload = {"model": request.model, "prompt": request.message, "stream": False}
    try:
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
        response.raise_for_status()
        ai_text = response.json().get("response", "Error procesando.")
    except Exception as e:
        ai_text = f"Error conectando con IA Local: {str(e)}"

    # 4. Guardar respuesta del asistente
    ai_msg = tablas.ChatMessage(session_id=session_id, role="assistant", content=ai_text, model_used=request.model)
    db.add(ai_msg)
    db.commit()

    return {"session_id": session_id, "response": ai_text}

@app.get("/admin/stats")
@app.get("/api/admin/stats")
def get_system_stats():
    # Monitorización en tiempo real con psutil
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return {"cpu": cpu, "ram": ram, "disk": disk}

@app.post("/agente/auditar")
@app.post("/api/agente/auditar")
def auditar_con_agente(request: ChatRequest):
    try:
        # Llamamos al script del agente en lugar de al chat normal
        resultado = ejecutar_agente_auditor(request.message)
        return {"status": "success", "agent_type": "Ciberseguridad", "response": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el Agente: {str(e)}")
