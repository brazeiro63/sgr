from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session
from app import crud, schemas, database, models
from app.dependencies import get_current_user
from typing import Optional

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/requisitos", tags=["Requisitos"])  # 🔹 Definindo prefixo

# 🚀 Criar um novo requisito
@router.post("/", response_model=schemas.RequisitoResponse)
def criar_requisito(
    requisito: schemas.RequisitoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Cria um novo requisito associado ao usuário autenticado."""
    print(f"Usuário autenticado para criação de requisito: {current_user.email}")  # 🔹 Debug

    novo_requisito = crud.criar_requisito(db, requisito, user_id=current_user.id)
    print(f"Requisito criado: {novo_requisito.titulo}")  # 🔹 Debug
    
    return novo_requisito

# 🚀 Listar requisitos do usuário autenticado
@router.get("/", response_model=list[schemas.RequisitoResponse])
def listar_requisitos(
    projeto_id: Optional[int] = Query(None, description="Filtrar requisitos por projeto"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Lista apenas os requisitos do usuário autenticado, podendo filtrar por projeto."""
    
    query = db.query(models.Requisito).filter(models.Requisito.user_id == current_user.id)

    if projeto_id:
        query = query.filter(models.Requisito.projeto_id == projeto_id)

    return query.all()

# 🚀 Obter um requisito específico
@router.get("/{requisito_id}", response_model=schemas.RequisitoResponse)
def obter_requisito(
    requisito_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Obtém um requisito pelo ID, garantindo que pertence ao usuário autenticado."""
    requisito = crud.obter_requisito(db, requisito_id)
    if not requisito or requisito.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Requisito não encontrado")
    return requisito

# 🚀 Atualizar um requisito
@router.put("/{requisito_id}", response_model=schemas.RequisitoResponse)
def atualizar_requisito(
    requisito_id: int,
    requisito: schemas.RequisitoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Atualiza um requisito apenas se o usuário autenticado for o dono."""
    requisito_atual = crud.obter_requisito(db, requisito_id)
    if not requisito_atual or requisito_atual.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ação não permitida")
    return crud.atualizar_requisito(db, requisito_id, requisito)

# 🚀 Excluir um requisito
@router.delete("/{requisito_id}")
def deletar_requisito(
    requisito_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Exclui um requisito apenas se pertence ao usuário autenticado."""
    requisito = crud.obter_requisito(db, requisito_id)
    if not requisito or requisito.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ação não permitida")
    return crud.deletar_requisito(db, requisito_id)

# 🚀 Alterar o estado do requisito
@router.put("/{requisito_id}/estado")
def atualizar_estado_requisito(
    requisito_id: int,
    estado_update: schemas.EstadoUpdate,  # ⬅️ Agora espera um objeto JSON no corpo
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    novo_estado = estado_update.novo_estado  # ⬅️ Acessa corretamente o estado

    """Altera o estado de um requisito seguindo as regras de transição."""

    # Obtém o requisito
    requisito = db.query(models.Requisito).filter(models.Requisito.id == requisito_id).first()

    if not requisito:
        raise HTTPException(status_code=404, detail="Requisito não encontrado")

    if current_user.role != models.RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Apenas administradores podem alterar o estado")

    estado_anterior = requisito.estado

    # 🚀 Regras de transição
    transicoes_validas = {
        "Proposto": ["Aprovado", "Rejeitado"],
        "Aprovado": ["Implementado"],
        "Implementado": ["Em Produção"],
        "Rejeitado": []  # Não pode ser alterado
    }

    if novo_estado.value not in transicoes_validas[estado_anterior.value]:
        raise HTTPException(
            status_code=400,
            detail=f"Transição inválida: {estado_anterior.value} → {novo_estado.value}"
        )

    # Atualiza o estado
    requisito.estado = novo_estado
    db.add(requisito)

    # Adiciona histórico
    historico = models.HistoricoRequisito(
        requisito_id=requisito.id,
        usuario_id=current_user.id,
        estado_anterior=estado_anterior,
        estado_novo=novo_estado
    )
    db.add(historico)

    db.commit()
    db.refresh(requisito)

    return requisito

# 🚀 Obter histórico de mudanças de estado de um requisito
@router.get("/{requisito_id}/historico", response_model=list[schemas.HistoricoRequisitoResponse])
def obter_historico_requisito(
    requisito_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Obtém o histórico de mudanças de estado de um requisito."""

    requisito = db.query(models.Requisito).filter(models.Requisito.id == requisito_id).first()

    if not requisito:
        raise HTTPException(status_code=404, detail="Requisito não encontrado")

    if requisito.usuario.id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas o dono do requisito pode ver o histórico")

    historico = db.query(models.HistoricoRequisito).filter(models.HistoricoRequisito.requisito_id == requisito_id).order_by(models.HistoricoRequisito.data_alteracao.desc()).all()

    return historico
