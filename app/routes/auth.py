from app import schemas, database, crud, security
from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, user_credentials.email)
    
    if not user or not security.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")

    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    return crud.create_user(db, user)

