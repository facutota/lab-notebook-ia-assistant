import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import models
from routes import proyectos, auth, experimentos, anotaciones, comentarios, health, perfil
from routes.admin import admin_proyectos, admin_usuarios, admin_experimentos, admin_anotaciones


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="API ALMA",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin_anotaciones.router)
app.include_router(admin_experimentos.router)
app.include_router(admin_usuarios.router)
app.include_router(admin_proyectos.router)
app.include_router(anotaciones.router)
app.include_router(comentarios.router)
app.include_router(experimentos.router)
app.include_router(health.router)
app.include_router(proyectos.router)
app.include_router(perfil.router)