from fastapi import FastAPI
from app import models, database, routes

app = FastAPI(title="Sistema de Gestão de Requisitos")

models.Base.metadata.create_all(bind=database.engine)

app.include_router(routes.router)

@app.get("/")
def root():
    return {"message": "Sistema de Gestão de Requisitos Ativo!"}
