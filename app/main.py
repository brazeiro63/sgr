from app import models, database, routes
from app.routes import auth, requisitos  # Importa a rota de autenticação
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Sistema de Gestão de Requisitos")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (pode ser restringido depois)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

models.Base.metadata.create_all(bind=database.engine)

# Adicionar as rotas
app.include_router(auth.router)  # Adiciona as rotas de autenticação
app.include_router(requisitos.router, prefix="/api")  # 🔹 Adicionando prefixo API

@app.get("/")
# def root():
#    return {"message": "Sistema de Gestão de Requisitos Ativo!"}

def listar_rotas():
    return [{"path": route.path, "name": route.name} for route in app.router.routes]
