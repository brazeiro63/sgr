from pydantic import BaseModel
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
        orm_mode = True
