from sqlalchemy.orm import Session
from app import models, schemas

def criar_requisito(db: Session, requisito: schemas.RequisitoCreate):
    db_requisito = models.Requisito(**requisito.dict())
    db.add(db_requisito)
    db.commit()
    db.refresh(db_requisito)
    return db_requisito

def obter_requisitos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Requisito).offset(skip).limit(limit).all()

def obter_requisito(db: Session, requisito_id: int):
    return db.query(models.Requisito).filter(models.Requisito.id == requisito_id).first()

def atualizar_requisito(db: Session, requisito_id: int, requisito: schemas.RequisitoCreate):
    db_requisito = db.query(models.Requisito).filter(models.Requisito.id == requisito_id).first()
    if db_requisito:
        for key, value in requisito.dict().items():
            setattr(db_requisito, key, value)
        db.commit()
        db.refresh(db_requisito)
    return db_requisito

def deletar_requisito(db: Session, requisito_id: int):
    db_requisito = db.query(models.Requisito).filter(models.Requisito.id == requisito_id).first()
    if db_requisito:
        db.delete(db_requisito)
        db.commit()
    return db_requisito
