from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/requisitos/", response_model=schemas.RequisitoResponse)
def criar_requisito(requisito: schemas.RequisitoCreate, db: Session = Depends(get_db)):
    return crud.criar_requisito(db, requisito)

@router.get("/requisitos/", response_model=list[schemas.RequisitoResponse])
def listar_requisitos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.obter_requisitos(db, skip, limit)

@router.get("/requisitos/{requisito_id}", response_model=schemas.RequisitoResponse)
def obter_requisito(requisito_id: int, db: Session = Depends(get_db)):
    return crud.obter_requisito(db, requisito_id)

@router.put("/requisitos/{requisito_id}", response_model=schemas.RequisitoResponse)
def atualizar_requisito(requisito_id: int, requisito: schemas.RequisitoCreate, db: Session = Depends(get_db)):
    return crud.atualizar_requisito(db, requisito_id, requisito)

@router.delete("/requisitos/{requisito_id}")
def deletar_requisito(requisito_id: int, db: Session = Depends(get_db)):
    return crud.deletar_requisito(db, requisito_id)
