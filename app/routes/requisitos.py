from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database, models
from app.dependencies import get_current_user

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/requisitos", tags=["Requisitos"])  # 🔹 Definindo prefixo


@router.post("/", response_model=schemas.RequisitoResponse)
def criar_requisito(
    requisito: schemas.RequisitoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Cria um novo requisito associado ao usuário autenticado."""
    print(f"Usuário autenticado para criação de requisito: {current_user.email}")  # 🔹 Debug

    novo_requisito = crud.criar_requisito(db, requisito, user_id=current_user.id)
    print(f"Requisito criado: {novo_requisito.titulo}")  # 🔹 Debug
    
    return novo_requisito

@router.get("/", response_model=list[schemas.RequisitoResponse])
def listar_requisitos(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Lista apenas os requisitos do usuário autenticado."""
    return db.query(models.Requisito).filter(models.Requisito.user_id == current_user.id).all()

@router.get("/{requisito_id}", response_model=schemas.RequisitoResponse)
def obter_requisito(
    requisito_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Obtém um requisito pelo ID, garantindo que pertence ao usuário autenticado."""
    requisito = crud.obter_requisito(db, requisito_id)
    if not requisito or requisito.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Requisito não encontrado")
    return requisito

@router.put("/{requisito_id}", response_model=schemas.RequisitoResponse)
def atualizar_requisito(
    requisito_id: int,
    requisito: schemas.RequisitoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Atualiza um requisito apenas se o usuário autenticado for o dono."""
    requisito_atual = crud.obter_requisito(db, requisito_id)
    if not requisito_atual or requisito_atual.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ação não permitida")
    return crud.atualizar_requisito(db, requisito_id, requisito)

@router.delete("/{requisito_id}")
def deletar_requisito(
    requisito_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Exclui um requisito apenas se pertence ao usuário autenticado."""
    requisito = crud.obter_requisito(db, requisito_id)
    if not requisito or requisito.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ação não permitida")
    return crud.deletar_requisito(db, requisito_id)
