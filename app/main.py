from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel
from exceptions import DatabaseException, NotFoundException
from db import engine
from routers import products, term_product, load_data

app = FastAPI(
    title="API - Prueba Técnica Sleakops",
    description="API Rest para saber el costo por hora/mensual/anual de una base de datos en particular.",
    version="1.0.0"
)

SQLModel.metadata.create_all(bind=engine)

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


@app.exception_handler(DatabaseException)
def database_exception_handler(request: Request, exc: DatabaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message}
    )


@app.exception_handler(NotFoundException)
def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message}
    )
