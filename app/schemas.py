from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


# 🚀 Esquema de Projeto Atualizado
class ProjetoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None  # 🔹 Introdução e Objetivo do Software
    escopo: Optional[str] = None  # 🔹 Escopo do Projeto

class ProjetoCreate(ProjetoBase):
    pass

class ProjetoResponse(ProjetoBase):
    id: int

    class Config:
        from_attributes = True


# 🚀 Enum para Estados dos Requisitos
class EstadoRequisitoEnum(str, Enum):
    PROPOSTO = "Proposto"
    APROVADO = "Aprovado"
    REJEITADO = "Rejeitado"
    IMPLEMENTADO = "Implementado"
    EM_PRODUCAO = "Em Produção"

class EstadoUpdate(BaseModel):
    novo_estado: EstadoRequisitoEnum

# 🚀 Schemas de Requisitos
class RequisitoBase(BaseModel):
    titulo: str
    descricao: str
    estado: EstadoRequisitoEnum = EstadoRequisitoEnum.PROPOSTO
    versao: Optional[str] = "1.0"
    projeto_id: int


class RequisitoCreate(RequisitoBase):
    pass

class RequisitoResponse(RequisitoBase):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes  = True

# 🚀 Schemas do Histórico de Estados
class HistoricoRequisitoResponse(BaseModel):
    id: int
    requisito_id: int
    usuario_id: int
    estado_anterior: EstadoRequisitoEnum
    estado_novo: EstadoRequisitoEnum
    data_alteracao: datetime

    class Config:
        from_attributes = True

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
