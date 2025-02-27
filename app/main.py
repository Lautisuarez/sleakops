from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init_db
from routers import products, term_product, load_data

@asynccontextmanager
async def lifespan(app: FastAPI):
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

app.include_router(load_data.router, prefix="/api/v1", tags=["Load Data"])
app.include_router(products.router, prefix="/api/v1", tags=["Product"])
app.include_router(term_product.router, prefix="/api/v1", tags=["Term to Product"])


