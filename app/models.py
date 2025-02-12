from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

# 🚀 Modelo de Usuário
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    requisitos = relationship("Requisito", back_populates="usuario")  # Relacionamento com requisitos

# 🚀 Modelo de Projeto
class Projeto(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    requisitos = relationship("Requisito", back_populates="projeto")  # Relacionamento reverso com requisitos

# 🚀 Modelo de Requisitos
class Requisito(Base):
    __tablename__ = "requisitos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    status = Column(String, default="Em Análise")
    versao = Column(String, default="1.0")
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))  # Chave estrangeira para User
    projeto_id = Column(Integer, ForeignKey("projetos.id"))  # Chave estrangeira para Projeto

    usuario = relationship("User", back_populates="requisitos")  # Relacionamento com User
    projeto = relationship("Projeto", back_populates="requisitos")  # Relacionamento com Projeto
