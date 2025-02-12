from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import database, models
from app.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Obtém o usuário autenticado a partir do token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        print(f"Recebendo token: {token}")  # 🔹 Depuração

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Payload: {payload}")  # 🔹 Depuração

        user_email = payload.get("sub")

        if user_email is None:
            print("Token sem `sub` válido!")  # 🔹 Depuração
            raise credentials_exception
        
        print(f"Usuário autenticado: {user_email}")  # 🔹 Debug

    except (JWTError, ValueError):
        print("Erro ao decodificar o token JWT")  # 🔹 Depuração
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == user_email).first()
    if user is None:
        raise credentials_exception

    print(f"Usuário encontrado: {user.name}")  # 🔹 Depuração
    return user
