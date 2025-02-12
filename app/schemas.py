from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class RequisitoBase(BaseModel):
    titulo: str
    descricao: str
    status: Optional[str] = "Em Análise"
    versao: Optional[str] = "1.0"
    projeto_id: int

class RequisitoCreate(RequisitoBase):
    pass

class RequisitoResponse(RequisitoBase):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes  = True

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  # Corrigindo para Pydantic V2

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
