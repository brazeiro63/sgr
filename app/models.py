from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from app.database import Base
import datetime
import enum

# Enum para definir os papéis
class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

# 🚀 Enum para Estados dos Requisitos
class EstadoRequisitoEnum(str, enum.Enum):
    PROPOSTO = "Proposto"
    APROVADO = "Aprovado"
    REJEITADO = "Rejeitado"
    IMPLEMENTADO = "Implementado"
    EM_PRODUCAO = "Em Produção"

# 🚀 Modelo de Usuário
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER)  # Usuário comum por padrão

    requisitos = relationship("Requisito", back_populates="usuario")

# 🚀 Modelo de Projeto (Atualizado)
class Projeto(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(Text, nullable=True)  # 🔹 Introdução e Objetivo do Software
    escopo = Column(Text, nullable=True)  # 🔹 Escopo do Projeto
    perpectiva = Column(Text, nullable=True)
    funcoes = Column(Text, nullable=True)
    restricoes = Column(Text, nullable=True)

    requisitos = relationship("Requisito", back_populates="projeto")


# 🚀 Modelo de Requisitos
class Requisito(Base):
    __tablename__ = "requisitos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    estado = Column(Enum(EstadoRequisitoEnum), default=EstadoRequisitoEnum.PROPOSTO, nullable=False)
    versao = Column(String, default="1.0")
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    projeto_id = Column(Integer, ForeignKey("projetos.id"))

    usuario = relationship("User", back_populates="requisitos")
    projeto = relationship("Projeto", back_populates="requisitos")
    historico = relationship("HistoricoRequisito", back_populates="requisito", cascade="all, delete-orphan")

# 🚀 Modelo de Histórico de Estados dos Requisitos
class HistoricoRequisito(Base):
    __tablename__ = "historico_requisitos"

    id = Column(Integer, primary_key=True, index=True)
    requisito_id = Column(Integer, ForeignKey("requisitos.id"))
    usuario_id = Column(Integer, ForeignKey("users.id"))
    estado_anterior = Column(Enum(EstadoRequisitoEnum), nullable=False)
    estado_novo = Column(Enum(EstadoRequisitoEnum), nullable=False)
    data_alteracao = Column(DateTime, default=datetime.datetime.utcnow)

    requisito = relationship("Requisito", back_populates="historico")
    usuario = relationship("User")
