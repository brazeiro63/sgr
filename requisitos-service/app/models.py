from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Requisito(Base):
    __tablename__ = "requisitos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    status = Column(String(50), default="Em Análise")
    versao = Column(String(10), default="1.0")
    projeto_id = Column(Integer, ForeignKey("projetos.id"))
    data_criacao = Column(DateTime, default=datetime.utcnow)

    projeto = relationship("Projeto", back_populates="requisitos")

class Projeto(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)

    requisitos = relationship("Requisito", back_populates="projeto")
