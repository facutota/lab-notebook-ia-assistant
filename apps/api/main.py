import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import Base, engine
import models
from routes import proyectos, auth, experimentos, anotaciones, comentarios, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="API ALMA",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(proyectos.router)
app.include_router(experimentos.router)
app.include_router(auth.router)
app.include_router(anotaciones.router)
app.include_router(comentarios.router)
app.include_router(health.router)

