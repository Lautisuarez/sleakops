from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init_db
from routers import products

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Inicializando Base de datos...")
    init_db()
    yield

app = FastAPI(
    title="API - Prueba Técnica Sleakops",
    description="API Rest para saber el costo por hora/mensual/anual de una base de datos en particular.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(products.router, prefix="/api/v1", tags=["Product"])



