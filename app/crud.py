from sqlalchemy.orm import Session
from app.models import User, Requisito 
from app import schemas, security, models

def criar_requisito(db: Session, requisito: schemas.RequisitoCreate, user_id: int):
    # Verifica se o projeto existe antes de criar o requisito
    projeto = db.query(models.Projeto).filter(models.Projeto.id == requisito.projeto_id).first()
    if not projeto:
        raise ValueError(f"Projeto com ID {requisito.projeto_id} não encontrado.")

    # Criação do novo requisito
    db_requisito = models.Requisito(**requisito.dict(), user_id=user_id)
    db.add(db_requisito)
    db.commit()
    db.refresh(db_requisito)
    return db_requisito


def obter_requisitos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Requisito).offset(skip).limit(limit).all()

def obter_requisito(db: Session, requisito_id: int):
    return db.query(Requisito).filter(Requisito.id == requisito_id).first()

def atualizar_requisito(db: Session, requisito_id: int, requisito: schemas.RequisitoCreate):
    db_requisito = db.query(Requisito).filter(Requisito.id == requisito_id).first()
    if db_requisito:
        for key, value in requisito.dict().items():
            setattr(db_requisito, key, value)
        db.commit()
        db.refresh(db_requisito)
    return db_requisito

def deletar_requisito(db: Session, requisito_id: int):
    db_requisito = db.query(Requisito).filter(Requisito.id == requisito_id).first()
    if db_requisito:
        db.delete(db_requisito)
        db.commit()
    return db_requisito

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.hash_password(user.password)
    db_user = User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()