from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.dependencies import get_current_user

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/projetos", tags=["Projetos"])

# 🚀 Criar um novo projeto
@router.post("/", response_model=schemas.ProjetoResponse)
def criar_projeto(projeto: schemas.ProjetoCreate, db: Session = Depends(get_db)):
    novo_projeto = models.Projeto(
        nome=projeto.nome,
        descricao=projeto.descricao,
        escopo=projeto.escopo,
    )
    db.add(novo_projeto)
    db.commit()
    db.refresh(novo_projeto)
    return novo_projeto

# 🚀 Atualizar um projeto existente
@router.put("/{projeto_id}", response_model=schemas.ProjetoResponse)
def atualizar_projeto(
    projeto_id: int,
    projeto: schemas.ProjetoCreate,
    db: Session = Depends(get_db),
):
    projeto_db = db.query(models.Projeto).filter(models.Projeto.id == projeto_id).first()

    if not projeto_db:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    projeto_db.nome = projeto.nome
    projeto_db.descricao = projeto.descricao
    projeto_db.escopo = projeto.escopo

    db.commit()
    db.refresh(projeto_db)
    return projeto_db

# 🚀 Obter um projeto específico
@router.get("/{projeto_id}", response_model=schemas.ProjetoResponse)
def obter_projeto(projeto_id: int, db: Session = Depends(get_db)):
    projeto = db.query(models.Projeto).filter(models.Projeto.id == projeto_id).first()
    
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    return projeto

@router.get("/", response_model=list[schemas.ProjetoResponse])
def listar_projetos(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Lista todos os projetos do usuário autenticado."""
    return db.query(models.Projeto).all()  # Alterar para filtrar por usuário, se necessário

@router.put("/{projeto_id}/editar", response_model=schemas.ProjetoResponse)
def atualizar_projeto(
    projeto_id: int,
    projeto: schemas.ProjetoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Atualiza o nome, descrição, escopo, perspectiva, funcoes e restrições do projeto"""
    db_projeto = db.query(models.Projeto).filter(models.Projeto.id == projeto_id).first()

    if not db_projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    db_projeto.nome = projeto.nome
    db_projeto.descricao = projeto.introducao
    db_projeto.escopo = projeto.escopo
    db_projeto.perpectiva = projeto.perspectiva
    db_projeto.funcoes = projeto.funcoes
    db_projeto.restricoes = projeto.restricoes

    db.commit()
    db.refresh(db_projeto)
    
    return db_projeto